from typing import Self, Callable
import random

from value import Value, ValueType
from probability import Probability
from condense import condense

class Variable:
    _data: Callable[[], list[tuple[Value, Probability, list[list[tuple[Self, Value]]]]]]
    _sample: Callable[[], Value]
    def __init__(self, a: Self | Value | ValueType | int | Callable[[], list[tuple[Value, Probability, list[list[tuple[Self, Value]]]]]],
                 b: None | int | tuple[Probability, Probability] = None):
        if isinstance(a, Variable):
            self._data = a._data
            self._sample = a._sample
        elif isinstance(a, Value):
            self._data = lambda: [(a, Probability(1, 1), [])]
            self._sample = lambda: a
        elif isinstance(a, Callable):
            self._data = a
            self._sample = lambda: random.sample(map(lambda x: x[0], a), 1)[0]
        elif isinstance(a, ValueType):
            if a is ValueType.Num or a is ValueType.Pair:
                raise ValueError("Number and pair types are not allowed!")
            if a is ValueType.Null:
                self._data = lambda: [(Value(), Probability(1, 1), [])]
                self._sample = lambda: Value()
            else:
                if not isinstance(b, tuple):
                    raise ValueError("Probability tuple required for generating a boolean variable!")
                self._data = lambda: [(Value(ValueType.Bool, False), b[0], []), (Value(ValueType.Bool, True), b[1], [])]
                self._sample = lambda: Value(ValueType.Bool, True) if random.random() > b[0] / (b[0] + b[1]) else Value(ValueType.Bool, False)
        else:
            if b is None:
                raise ValueError("Only one integer given as parameter!")
            self._data = lambda: [(Value(ValueType.Num, x), Probability(1, b - a + 1), []) for x in range(a, b + 1, 1)]
            self._sample = lambda: random.sample(range(a, b + 1), 1)[0]

    def pair(self, other: Self) -> Self:
        return Variable(ValueType.Null) # placeholder; TODO finish entanglement

    def __add__(self, other: Self) -> Self:
        return Variable(lambda: condense(map(lambda x: (x[0][0] + x[0][1], x[1], x[2]), self.pair(other)._data())))
    
    def __sub__(self, other: Self) -> Self:
        return Variable(lambda: condense(map(lambda x: (x[0][0] - x[0][1], x[1], x[2]), self.pair(other)._data())))
    
    def ternary(self, true: Self, false: Self) -> Self:
        return Variable(lambda: condense(map(lambda x: (x[0][1][1] if x[0][0] else x[0][1][0], x[1], x[2]), self.pair(true.pair(false))._data())))
    
    def first(self) -> Self:
        return Variable(lambda: condense(map(lambda x: (x[0][0], x[1], x[2]), self._data())))
    
    def second(self) -> Self:
        return Variable(lambda: condense(map(lambda x: (x[0][1], x[1], x[2]), self._data())))
    
    def __matmul__(self, other) -> Self:
        return Variable(lambda:
                        condense(map(lambda x:
                            random.sample(range(x[0][0].check(ValueType.Num)[0], x[0][1].check(ValueType.Num)[0] + 1), 1)[0],
                            self.pair(other)._data()
                            )
                        ))
    
    def l_and(self, other: Self) -> Self:
        return Variable(lambda: condense(map(lambda x: (Value(ValueType.Bool, x[0][0] and x[0][1]), x[1], x[2]), self.pair(other)._data())))
    
    def l_or(self, other: Self) -> Self:
        return Variable(lambda: condense(map(lambda x: (Value(ValueType.Bool, x[0][0] or x[0][1]), x[1], x[2]), self.pair(other)._data())))
    
    def l_not(self) -> Self:
        return Variable(lambda: condense(map(lambda x: (Value(ValueType.Bool, not x[0]), x[1], x[2]), self._data())))
