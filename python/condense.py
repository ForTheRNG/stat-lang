from functools import reduce
from typing import Iterable

from value import Value
from probability import Probability
from variable import Variable

def _add(a: list[tuple[Value, Probability, list[list[tuple[Variable, Value]]]]],
         e: tuple[Value, Probability, list[list[tuple[Variable, Value]]]]
         ) -> list[tuple[Value, Probability, list[list[tuple[Variable, Value]]]]]:
    pa = list(map(lambda x: x[0], a))
    if e[0] in pa:
        idx = pa.index(e[0])
        a[idx] = (e[0], a[idx][1] + e[1], a[idx][2].extend(e[2]))
    else:
        a.append(e)
    return a


def condense(a: Iterable[tuple[Value, Probability, list[list[tuple[Variable, Value]]]]]
             ) -> list[tuple[Value, Probability, list[list[tuple[Variable, Value]]]]]:
    return reduce(_add, list(a), [])