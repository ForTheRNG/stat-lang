from copy import copy
from functools import reduce
from typing import Iterable
from random import randint

from .value import Value, ValueType
from .probability import Probability

def find(arr: list[tuple[Value, Probability, list]], e: Value) -> int:
    pa = list(map(lambda x: x[0], arr))
    idx = -1
    try:
        idx = pa.index(e)
    except ValueError:
        pass
    return idx

def _add(a: list[tuple[Value, Probability, list]],
         e: tuple[Value, Probability, list]
         ) -> list[tuple[Value, Probability, list]]:
    idx = find(a, e[0])
    if idx != -1:
        l = copy(a[idx][2])
        l.extend(e[2])
        a[idx] = (e[0], a[idx][1] + e[1], l)
    else:
        if e[1]._num != 0:
            a.append(e)
    return a


def condense(a: Iterable[tuple[Value, Probability, list]]
             ) -> list[tuple[Value, Probability, list]]:
    return reduce(_add, a, [])

def prob_gen(a: int, b: int) -> list[int]:
    if a == 0:
        return [1]
    initial_list = prob_gen(a - 1, b)
    final_list = []
    sum = 0
    for x in range(b):
        sum += initial_list[x]
        final_list.append(sum)
    for x in range(b, len(initial_list) - b):
        sum -= initial_list[x - b]
        sum += initial_list[x]
        final_list.append(sum)
    for x in range(len(initial_list) - b, len(initial_list)):
        sum -= initial_list[x - b]
        final_list.append(sum)
    return final_list

def extend(a: list[tuple[Value, Probability, list]],
            x: tuple[Value, Probability, list]
            ) -> list[tuple[Value, Probability, list]]:
    c = x[0][1].check(ValueType.Num)[0]
    d = x[0][2].check(ValueType.Num)[0]
    p = d ** c
    a.extend((Value(ValueType.Num, i), x[1] * Probability(j, p), x[2]) for i, j in enumerate(prob_gen(c, d), c))
    return a

def die_roll(a: int, b: int) -> int:
    if a == 0:
        return 0
    return randint(1, b) + die_roll(a - 1, b)
