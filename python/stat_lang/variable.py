from functools import reduce
from typing import Any, Callable, Iterable, Literal, Self

from .value import Value, ValueType
from .probability import Probability
from .helpers import condense, die_roll, extend, prob_gen

class Variable:
    __data: Callable[[], list[tuple[Value, Probability, list[list[tuple[Self, Value]]]]]]
    """Create the distribution of the variable. Stored as a lambda for lazy evaluation."""
    __sample: Callable[[], Value]
    """Sample the variable. Ignores sampling ID."""
    _sample_cache: tuple[int, Value]
    """Sample cache; saves both sample id and actual result for dependency graphs."""
    _data_cache: list[tuple[Value, Probability, list[list[tuple[Self, Value]]]]] | Literal[""]
    """Data cache; saves result for re-computations in a dependency graph."""
    _sample_id: int = 0
    """Needed to ensure the same sample gives the same result for the same variable."""

    def __init__(self, a: Self | Value | ValueType | int | Callable[[], list[tuple[Value, Probability, list[list[tuple[Self, Value]]]]]],
                 b: None | int | bool | tuple[Value, Value] | Callable[[int], Value] = None):
        """
        Initialize a new variable.

        If a is another Variable, a copy operation is performed. b is ignored.

        If a is a ValueType, b should be an object of that type. A variable will be created with one outcome, b.

        If a is an int, b should be an int. A new variable will be created as the sum of a dice with b faces.

        If a is a lambda function, it is expected to return an internal representation of a variable. b should be a correct sampling of that data, also as a lambda function.
        """
        self._sample_cache = -1, None
        self._data_cache = ""
        if isinstance(a, Variable):
            self.__data = a._data
            self._sample = a._sample
        elif isinstance(a, Value):
            self.__data = lambda: [(a, Probability(1, 1), [])]
            self._sample = lambda: a
        elif isinstance(a, Callable):
            self.__data = a
            self.__sample = b
        elif isinstance(a, ValueType):
            self.__data = lambda: [(Value(a, b), Probability(1, 1), [])]
            self.__sample = lambda: Value(a, b)
        else:
            p = b ** a
            self.__data = lambda: [(Value(ValueType.Num, x[0]), Probability(x[1], p), []) for x in enumerate(prob_gen(a, b), a)]
            self.__sample = lambda: die_roll(a, b)

    def analyze(self) -> list[tuple[Any, float]]:
        """Return a list of tuples of outcomes and associeted probabilities."""
        if self._data_cache == "":
            self._data_cache = self._data()
        return list(map(lambda x: (x[0]._data, x[1]._num / x[1]._den), self._data_cache))

    def __getitem__(self, _) -> Value:
        """Sample the variable. No specific outcome; the key is a filler parameter."""
        Variable._sample_id += 1
        if Variable._sample_id == 1 << 30:
            Variable._sample_id = 0
        return self._get_sample()
    
    def sample(self) -> Value:
        """Sample the variable."""
        return self[0]

    def _data(self) -> list[tuple[Value, Probability, list[list[tuple[Self, Value]]]]]:
        """Get the data from the lambda."""
        if self._data_cache == "":
            self._data_cache = self.__data()
        return self._data_cache

    def _sample(self) -> Value:
        """Sample a value. Includes sampling ID."""
        if Variable._sample_id != self._sample_cache[0]:
            self._sample_cache = Variable._sample_id, self.__sample()
        return self._sample_cache[1]

    def pair(self, other: Self) -> Self:
        """Pair two variables together in a tuple."""
        return Variable(lambda: map(lambda x, y: (Value(ValueType.Pair, (x[0], y[0])), x[1] * y[1], []), self._data(), other._data()),
                        lambda: Value(ValueType.Pair, (self._sample(), other._sample()))) # TODO finish entanglement properly

    # TODO add the other operations
    def __add__(self, other: Self) -> Self:
        if not isinstance(other, Variable):
            other = Variable(ValueType.Num, other)
        return Variable(lambda: map(lambda x: (x[0][1] + x[0][2], x[1], x[2]), self.pair(other)._data()),
                        lambda: self._sample() + other._sample())
    
    def __sub__(self, other: Self) -> Self:
        if not isinstance(other, Variable):
            other = Variable(ValueType.Num, other)
        return Variable(lambda: map(lambda x: (x[0][1] - x[0][2], x[1], x[2]), self.pair(other)._data()),
                        lambda: self._sample() - other._sample())

    def __mul__(self, other: Self) -> Self:
        if not isinstance(other, Variable):
            other = Variable(ValueType.Num, other)
        return Variable(lambda: map(lambda x: (x[0][1] * x[0][2], x[1], x[2]), self.pair(other)._data()),
                        lambda: self._sample() * other._sample())
    
    def __div__(self, other: Self) -> Self:
        if not isinstance(other, Variable):
            other = Variable(ValueType.Num, other)
        return Variable(lambda: map(lambda x: (x[0][1] / x[0][2], x[1], x[2]), self.pair(other)._data()),
                        lambda: self._sample() // other._sample())
    
    def ternary(self, true: Self, false: Self) -> Self:
        """Compute a ternary output with the main variable as the condition."""
        if not isinstance(true, Variable):
            true = Variable(ValueType.Num, true)
        if not isinstance(false, Variable):
            false = Variable(ValueType.Num, false)
        return Variable(lambda: map(lambda x: (x[0][2][2] if x[0][1] else x[0][2][1], x[1], x[2]), self.pair(true.pair(false))._data()),
                        lambda: true._sample() if self._sample() else false._sample())
    
    def first(self) -> Self:
        """Get the first element in a paired variable."""
        return Variable(lambda: map(lambda x: (x[0][1], x[1], x[2]), self._data()),
                        lambda: self._sample()[0])
    
    def second(self) -> Self:
        """Get the second element in a paired variable."""
        return Variable(lambda: map(lambda x: (x[0][2], x[1], x[2]), self._data()),
                        lambda: self._sample()[1])
    
    def __matmul__(self, other: Self) -> Self:
        return Variable(lambda: reduce(extend, self.pair(other)._data(), []),
                        lambda: Value(ValueType.Num, die_roll(self._sample().check(ValueType.Num)._data, other._sample().check(ValueType.Num)._data)))
    
    def l_and(self, other: Self) -> Self:
        """Perform logical AND on two variables."""
        return Variable(lambda: map(lambda x: (Value(ValueType.Bool, x[0][1] and x[0][2]), x[1], x[2]), self.pair(other)._data()),
                        lambda: Value(ValueType.Bool, self._sample() and other._sample()))
    
    def l_or(self, other: Self) -> Self:
        """Perform logical OR on two variables."""
        return Variable(lambda: map(lambda x: (Value(ValueType.Bool, x[0][1] or x[0][2]), x[1], x[2]), self.pair(other)._data()),
                        lambda: Value(ValueType.Bool, self._sample() or other._sample()))
    
    def l_not(self) -> Self:
        """Perform logical NOT on the variable."""
        return Variable(lambda: map(lambda x: (Value(ValueType.Bool, not x[0]), x[1], x[2]), self._data()),
                        lambda: Value(ValueType.Bool, not self._sample()))

    def c_lt(self, other: Self) -> Self:
        """Compare two variables using "less than" logic."""
        return Variable(lambda: map(lambda x: (Value(ValueType.Bool, x[0][1] < x[0][2]), x[1], x[2]), self.pair(other)._data()),
                        lambda: Value(ValueType.Bool, self._sample() < other._sample()))