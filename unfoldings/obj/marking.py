from __future__ import annotations

from . import place

from collections import Counter

from typing import Mapping, overload, Iterable, Iterator


class Marking(Mapping[place.Place, int]):
    @overload
    def __init__(self) -> None:
        pass

    @overload
    def __init__(self, iterable: Iterable[place.Place]) -> None:
        pass

    def __init__(self, iterable: Iterable[place.Place] | None = None) -> None:
        self.__counter: Counter[place.Place]
        if isinstance(iterable, Counter):
            self.__counter = iterable
        elif isinstance(iterable, Marking):
            self.__counter = iterable.__counter
        else:
            self.__counter = Counter(iterable)

    def __getitem__(self, __key: place.Place) -> int:
        return self.__counter[__key]

    def __len__(self) -> int:
        return len(self.__counter)

    def __iter__(self) -> Iterator[place.Place]:
        return iter(self.__counter)

    def __sub__(self, other: Marking) -> Marking:
        return Marking(self.__counter - other.__counter)

    def __hash__(self) -> int:
        power_of_2 = 1

        res = 0
        for i, (k, v) in enumerate(self.items(), 1):
            if i == power_of_2:
                res += ((31 + power_of_2) ^ 2000) * hash(k) * v
                power_of_2 *= 2

        return res

    def elements(self) -> Iterable[place.Place]:
        return self.__counter.elements()
