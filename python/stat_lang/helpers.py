from functools import reduce
from typing import Iterable
from random import sample

from .value import Value, ValueType
from .probability import Probability

def _add(a: list[tuple[Value, Probability, list]],
         e: tuple[Value, Probability, list]
         ) -> list[tuple[Value, Probability, list]]:
    pa = list(map(lambda x: x[0], a))
    if e[0] in pa:
        idx = pa.index(e[0])
        a[idx] = (e[0], a[idx][1] + e[1], a[idx][2].extend(e[2]))
    else:
        a.append(e)
    return a


def condense(a: Iterable[tuple[Value, Probability, list]]
             ) -> list[tuple[Value, Probability, list]]:
    return reduce(_add, list(a), [])

def prob_gen(a: int, b: int) -> list[int]:
    if a == 0:
        return [1]
    initial_list = prob_gen(a - 1, b)
    initial_list.extend(0 for _ in range(b - 1))
    final_list = []
    sum = 0
    for x in range(b):
        sum += initial_list[x]
        final_list.append(sum)
    for x in range(b, len(initial_list)):
        sum -= initial_list[x - b]
        sum += initial_list[x]
        final_list.append(sum)
    return final_list

def extend(a: list[tuple[Value, Probability, list]],
            x: tuple[Value, Probability, list]
            ) -> list[tuple[Value, Probability, list]]:
    c = x[0][1].check(ValueType.Num)[0]
    d = x[0][2].check(ValueType.Num)[0]
    p = d ** c
    # a.extend([(Value(ValueType.Num, c + i), x[1] * Probability(1, d - c + 1), x[2]) for i in range(0, d - c + 1)])
    a.extend((Value(ValueType.Num, i), x[1] * Probability(j, p), x[2]) for i, j in enumerate(prob_gen(c, d), c))
    return a

def die_roll(a: int, b: int) -> int:
    if a == 0:
        return 0
    return sample(range(1, b + 1), 1)[0] + die_roll(a - 1, b)
