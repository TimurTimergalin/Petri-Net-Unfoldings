from __future__ import annotations

from . import place

from collections import Counter


class Marking(Counter[place.Place]):
    def __hash__(self) -> int:
        power_of_2 = 1

        res = 0
        for i, (k, v) in enumerate(self.items(), 1):
            if i == power_of_2:
                res += ((31 + power_of_2) ^ 2000) * hash(k) * v
                power_of_2 *= 2

        return res
