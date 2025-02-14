from typing import Self
from enum import Enum

class ValueType(Enum):
    Null = 0
    Bool = 1
    Num = 2
    Pair = 3

class Value:
    type: ValueType
    data: None | bool | int | tuple[Self, Self]

    def __init__(self, type: None | ValueType = None, data: None | bool | int | Self = None, second: None | Self = None):
        if type is None:
            type = ValueType.Null
        self.type = type
        if type is ValueType.Null:
            self.data = None
        elif type is ValueType.Bool:
            self.data = bool(data)
        elif type is ValueType.Num:
            self.data = int(data)
        elif type is ValueType.Pair:
            self.data = data, second
        else:
            raise ValueError("Value type was not part of ValueType enum!")

    def __add__(self, other: Self) -> Self:
        if self.type is not ValueType.Num and other.type is not ValueType.Num:
            raise ValueError("Value is not number!")
        return Value(ValueType.Num, self.data + other.data)
    
    def __sub__(self, other: Self) -> Self:
        if self.type is not ValueType.Num and other.type is not ValueType.Num:
            raise ValueError("Value is not number!")
        return Value(ValueType.Num, self.data - other.data)
    
    def __mul__(self, other: Self) -> Self:
        if self.type is not ValueType.Num and other.type is not ValueType.Num:
            raise ValueError("Value is not number!")
        return Value(ValueType.Num, self.data * other.data)
    
    def __truediv__(self, other: Self) -> Self:
        if self.type is not ValueType.Num and other.type is not ValueType.Num:
            raise ValueError("Value is not number!")
        return Value(ValueType.Num, self.data / other.data)
    
    def __lt__(self, other: Self) -> bool:
        if self.type is not ValueType.Num and other.type is not ValueType.Num:
            raise ValueError("Value is not number!")
        return Value(ValueType.Num, self.data < other.data)
    
    def __gt__(self, other: Self) -> bool:
        if self.type is not ValueType.Num and other.type is not ValueType.Num:
            raise ValueError("Value is not number!")
        return Value(ValueType.Num, self.data > other.data)
    
    def __le__(self, other: Self) -> bool:
        if self.type is not ValueType.Num and other.type is not ValueType.Num:
            raise ValueError("Value is not number!")
        return Value(ValueType.Num, self.data <= other.data)

    def __ge__(self, other: Self) -> bool:
        if self.type is not ValueType.Num and other.type is not ValueType.Num:
            raise ValueError("Value is not number!")
        return Value(ValueType.Num, self.data >= other.data)

    def __eq__(self, other: Self) -> bool:
        if self.type is not ValueType.Num and other.type is not ValueType.Num:
            raise ValueError("Value is not number!")
        return Value(ValueType.Num, self.data == other.data)

    def __ne__(self, other: Self) -> bool:
        if self.type is not ValueType.Num and other.type is not ValueType.Num:
            raise ValueError("Value is not number!")
        return Value(ValueType.Num, self.data != other.data)
    
    def __neg__(self) -> Self:
        if self.type is not ValueType.Num:
            raise ValueError("Value is not number!")
        return Value(ValueType.Num, -self.data)

    def __bool__(self) -> bool:
        if self.type is not ValueType.Bool:
            raise ValueError("Value is not boolean!")
        return self.data