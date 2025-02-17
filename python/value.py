from typing import Self
from enum import Enum

class ValueType(Enum):
    Null = "null"
    Bool = "boolean"
    Num = "number"
    Pair = "pair"

class Value:
    _type: ValueType
    _data: None | bool | int | tuple[Self, Self]

    def __init__(self, type: None | ValueType = None, data: None | bool | int | Self = None, second: None | Self = None):
        if type is None:
            type = ValueType.Null
        self._type = type
        if type is ValueType.Null:
            self._data = None
        elif type is ValueType.Bool:
            self._data = bool(data)
        elif type is ValueType.Num:
            self._data = int(data)
        elif type is ValueType.Pair:
            self._data = data, second
        else:
            raise ValueError("Value type was not part of ValueType enum!")

    def check(self, type: ValueType) -> Self:
        if self._type is not type:
            raise ValueError(f"Value is not a {type.value}!")
        return self

    def __getitem__(self, key: int | None) -> Self:
        if key == 0 or key == None:
            return self._data[0] if self._type == ValueType.Pair else self._data
        if key > 1 or key < 0:
            raise ValueError("Key is not 0 or 1!")
        if key == 1 and self._type != ValueType.Pair:
            raise ValueError("Cannot access second element of a non-pair!")
        return self._data[1]

    def __add__(self, other: Self) -> Self:
        return Value(ValueType.Num, self.check(ValueType.Num)._data + other.check(ValueType.Num)._data)
    
    def __sub__(self, other: Self) -> Self:
        return Value(ValueType.Num, self.check(ValueType.Num)._data - other.check(ValueType.Num)._data)
    
    def __mul__(self, other: Self) -> Self:
        return Value(ValueType.Num, self.check(ValueType.Num)._data * other.check(ValueType.Num)._data)
    
    def __truediv__(self, other: Self) -> Self:
        return Value(ValueType.Num, self.check(ValueType.Num)._data // other.check(ValueType.Num)._data)
    
    def __lt__(self, other: Self) -> bool:
        return Value(ValueType.Num, self.check(ValueType.Num)._data < other.check(ValueType.Num)._data)
    
    def __gt__(self, other: Self) -> bool:
        return Value(ValueType.Num, self.check(ValueType.Num)._data > other.check(ValueType.Num)._data)
    
    def __le__(self, other: Self) -> bool:
        return Value(ValueType.Num, self.check(ValueType.Num)._data <= other.check(ValueType.Num)._data)

    def __ge__(self, other: Self) -> bool:
        return Value(ValueType.Num, self.check(ValueType.Num)._data >= other.check(ValueType.Num)._data)

    def __eq__(self, other: Self) -> bool:
        return self._type == other._type and (
            self._type == ValueType.Null or (
                self._data[0] == other._data[0] and self._data[1] == other._data[1]
                if self.type == ValueType.Pair
                else self._data == other._data
            )
        )

    def __ne__(self, other: Self) -> bool:
        return not (self == other)
    
    def __neg__(self) -> Self:
        return Value(ValueType.Num, -self.check(ValueType.Num)._data)

    def __bool__(self) -> bool:
        return self.check(ValueType.Bool)._data