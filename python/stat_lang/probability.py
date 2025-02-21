from typing import Self
from math import gcd

class Probability:
    _num: int
    _den: int

    def __init__(self, numerator: int, denominator: int):
        if (denominator < 0):
            numerator = -numerator
            denominator = -denominator
        g = gcd(numerator, denominator)
        self._num = numerator // g
        self._den = denominator // g
    
    def __add__(self, other: Self) -> Self:
        a = self._num * other._den + self._den * other._num
        b = self._den * other._den
        g = gcd(a, b)
        return Probability(a // g, b // g)
    
    def __sub__(self, other: Self) -> Self:
        a = self._num * other._den - self._den * other._num
        b = self._den * other._den
        g = gcd(a, b)
        return Probability(a // g, b // g)
    
    def __mul__(self, other: Self) -> Self:
        a = self._num * other._num
        b = self._den * other._den
        g = gcd(a, b)
        return Probability(a // g, b // g)
    
    def __truediv__(self, other: Self) -> Self:
        a = self._num * other._den
        b = self._den * other._num
        g = gcd(a, b)
        return Probability(a // g, b // g)
    
    def __lt__(self, other: Self) -> bool:
        return self._num * other._den < self._den * other._num
    
    def __gt__(self, other: Self) -> bool:
        return self._num * other._den > self._den * other._num
    
    def __le__(self, other: Self) -> bool:
        return self._num * other._den <= self._den * other._num

    def __ge__(self, other: Self) -> bool:
        return self._num * other._den >= self._den * other._num

    def __eq__(self, other: Self) -> bool:
        return self._num == other._num and self._den == other._den

    def __ne__(self, other: Self) -> bool:
        return self._num != other._num or self._den != other._den
    
    def __neg__(self) -> Self:
        return Probability(-self._num, self._den)