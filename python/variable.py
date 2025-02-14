from typing import Self, Callable

from value import Value, ValueType
from probability import Probability

class Variable:
    data: Callable[[], list[tuple[Value, Probability, list[tuple[Self, Value]]]]]
    def __init__(self, a: Self | Value | ValueType | int | Callable[[], list[tuple[Value, Probability, list[tuple[Self, Value]]]]],
                 b: None | int | tuple[Probability, Probability] = None):
        if isinstance(a, Variable):
            self.data = a.data
        elif isinstance(a, Value):
            self.data = lambda: [(a, Probability(1, 1), [])]
        elif isinstance(a, Callable):
            self.data = a
        elif isinstance(a, ValueType):
            if a is ValueType.Num or a is ValueType.Pair:
                raise ValueError("Number and pair types are not allowed!")
            if a is ValueType.Null:
                self.data = lambda: [(Value(), Probability(1, 1), [])]
            else:
                if not isinstance(b, tuple):
                    raise ValueError("Probability tuple required for generating a boolean variable!")
                self.data = lambda: [(Value(ValueType.Bool, False), b[0], []), (Value(ValueType.Bool, True), b[1], [])]
        else:
            if b is None:
                raise ValueError("Only one integer given as parameter!")
            self.data = lambda: [(Value(ValueType.Num, x), Probability(1, b - a + 1), []) for x in range(a, b + 1, 1)]

    def __add__(self, other: Self) -> Self:
        return Variable(ValueType.Null) # placeholder