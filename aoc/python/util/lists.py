from __future__ import annotations
from typing import TypeVar

_T = TypeVar('_T')


# Taken from #adventofcode-spoilers -- by mjsir911
def clump(l: list[_T], n) -> 'zip[tuple[_T, ...]]':
    return zip(*[l[i:] for i in range(n)])
