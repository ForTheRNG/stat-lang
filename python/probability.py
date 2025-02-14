from typing import Self
from math import gcd

class Probability:
    num: int
    den: int

    def __init__(self, numerator: int, denumerator: int):
        if (denumerator < 0):
            numerator = -numerator
            denumerator = -denumerator
        self.num = numerator
        self.den = denumerator
    
    def __add__(self, other: Self) -> Self:
        a = self.num * other.den + self.den * other.num
        b = self.den * other.den
        g = gcd(a, b)
        return Probability(a / g, b / g)
    
    def __sub__(self, other: Self) -> Self:
        a = self.num * other.den - self.den * other.num
        b = self.den * other.den
        g = gcd(a, b)
        return Probability(a / g, b / g)
    
    def __mul__(self, other: Self) -> Self:
        a = self.num * other.num
        b = self.den * other.den
        g = gcd(a, b)
        return Probability(a / g, b / g)
    
    def __truediv__(self, other: Self) -> Self:
        a = self.num * other.den
        b = self.den * other.num
        g = gcd(a, b)
        return Probability(a / g, b / g)
    
    def __lt__(self, other: Self) -> bool:
        return self.num * other.den < self.den * other.num
    
    def __gt__(self, other: Self) -> bool:
        return self.num * other.den > self.den * other.num
    
    def __le__(self, other: Self) -> bool:
        return self.num * other.den <= self.den * other.num

    def __ge__(self, other: Self) -> bool:
        return self.num * other.den >= self.den * other.num

    def __eq__(self, other: Self) -> bool:
        return self.num == other.num and self.den == other.den

    def __ne__(self, other: Self) -> bool:
        return self.num != other.num or self.den != other.den
    
    def __neg__(self) -> Self:
        return Probability(-self.num, self.den)