from functools import reduce
from typing import Any, Self, Callable
from random import random

from value import Value, ValueType
from probability import Probability
from helpers import condense, die_roll, extend, prob_gen

_sample_id: int = 0

class Variable:
    _data: Callable[[], list[tuple[Value, Probability, list[list[tuple[Self, Value]]]]]]
    sample: Callable[[], Value]
    _cache: tuple[int, Value]
    _data_cache: list[tuple[Value, Probability, list[list[tuple[Self, Value]]]]] | None

    def _sample_lambda(self, l: Callable[[], Value]) -> Value:
        if self._cache[0] != _sample_id:
            self._cache = _sample_id, l()
        return self._cache[1]
    
    def analyze(self) -> list[tuple[Value, Probability]]:
        if self._data_cache is None:
            self._data_cache = self._data()
        return list(map(lambda x: (x[0], x[1]), self._data_cache))

    def __init__(self, a: Self | Value | ValueType | int | Callable[[], list[tuple[Value, Probability, list[list[tuple[Self, Value]]]]]],
                 b: None | int | tuple[Probability, Probability] | Callable[[int], Value] = None):
        if isinstance(a, Variable):
            self._data = a._data
            self.sample = a.sample
        elif isinstance(a, Value):
            self._data = lambda: [(a, Probability(1, 1), [])]
            self.sample = lambda: a
        elif isinstance(a, Callable):
            self._data = a
            self.sample = self._sample_lambda(b)
        elif isinstance(a, ValueType):
            if a is ValueType.Num or a is ValueType.Pair:
                raise ValueError("Number and pair types are not allowed!")
            if a is ValueType.Null:
                self._data = lambda: [(Value(), Probability(1, 1), [])]
                self.sample = lambda: Value()
            else:
                if not isinstance(b, tuple):
                    raise ValueError("Probability tuple required for generating a boolean variable!")
                self._data = lambda: [(Value(ValueType.Bool, False), b[0], []), (Value(ValueType.Bool, True), b[1], [])]
                self.sample = lambda: Value(ValueType.Bool, True) if random() > b[0] / (b[0] + b[1]) else Value(ValueType.Bool, False)
        else:
            if b is None:
                self._data = lambda: [(Value(ValueType.Num, a), Probability(1, 1), [])]
                self.sample = lambda: Value(ValueType.Num, a)
            p = b ** a
            self._data = lambda: [(Value(ValueType.Num, x[0]), Probability(x[1], p), []) for x in enumerate(prob_gen(a, b), a)]
            self.sample = lambda: die_roll(a, b)

    def __getitem__(self, key: Any) -> Value:
        _sample_id += 1
        if _sample_id == 2 ** 30:
            _sample_id = 0
        return self.sample()

    def pair(self, other: Self) -> Self:
        return Variable(ValueType.Null) # placeholder; TODO finish entanglement

    def __add__(self, other: Self) -> Self:
        return Variable(lambda: condense(map(lambda x: (x[0][0] + x[0][1], x[1], x[2]), self.pair(other)._data())),
                        lambda: self.sample() + other.sample())
    
    def __sub__(self, other: Self) -> Self:
        return Variable(lambda: condense(map(lambda x: (x[0][0] - x[0][1], x[1], x[2]), self.pair(other)._data())),
                        lambda: self.sample() - other.sample())
    
    def ternary(self, true: Self, false: Self) -> Self:
        return Variable(lambda: condense(map(lambda x: (x[0][1][1] if x[0][0] else x[0][1][0], x[1], x[2]), self.pair(true.pair(false))._data())),
                        lambda: true.sample() if self.sample() else false.sample())
    
    def first(self) -> Self:
        return Variable(lambda: condense(map(lambda x: (x[0][0], x[1], x[2]), self._data())),
                        lambda: self.sample()[0])
    
    def second(self) -> Self:
        return Variable(lambda: condense(map(lambda x: (x[0][1], x[1], x[2]), self._data())),
                        lambda: self.sample()[1])
    
    def __matmul__(self, other: Self) -> Self:
        return Variable(lambda: condense(reduce(extend, self.pair(other)._data(), [])),
                        lambda: Value(ValueType.Num, die_roll(self.sample().check(ValueType.Num)._data, other.sample().check(ValueType.Num)._data)))
    
    def l_and(self, other: Self) -> Self:
        return Variable(lambda: condense(map(lambda x: (Value(ValueType.Bool, x[0][0] and x[0][1]), x[1], x[2]), self.pair(other)._data())),
                        lambda: Value(ValueType.Bool, self.sample() and other.sample()))
    
    def l_or(self, other: Self) -> Self:
        return Variable(lambda: condense(map(lambda x: (Value(ValueType.Bool, x[0][0] or x[0][1]), x[1], x[2]), self.pair(other)._data())),
                        lambda: Value(ValueType.Bool, self.sample() or other.sample()))
    
    def l_not(self) -> Self:
        return Variable(lambda: list(map(lambda x: (Value(ValueType.Bool, not x[0]), x[1], x[2]), self._data())),
                        lambda: Value(ValueType.Bool, not self.sample()))
