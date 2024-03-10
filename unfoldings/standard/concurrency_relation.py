from __future__ import annotations
from ..prefix_obj import Event, Condition

from itertools import product
from typing import Generator
from functools import reduce

from ..typing_utils import not_none


class Co:
    def __init__(self) -> None:
        self.__pairs: set[tuple[Condition, Condition]] = set()

    def __call__(self, a: Condition, b: Condition) -> bool:
        return (a, b) in self.__pairs

    def update(self, new_event: Event, conditions: set[Condition]) -> None:
        new = set(x for x, _ in new_event.postset)
        old = conditions - new

        concurrent_with: set[Condition] = set()

        for c in old:
            for c1, _ in new_event.preset:
                if not self(c, c1) or c == c1:
                    break
            else:
                concurrent_with.add(c)

        self.__pairs.update(product(new, new))
        self.__pairs.update(product(new, concurrent_with))
        self.__pairs.update(product(concurrent_with, new))

    def new_co_sets(self, new: Event) -> Generator[tuple[Condition, ...], None, None]:
        new_post_set = set(x for x, _ in new.postset)

        def sort_key(x: tuple[Condition, Condition]) -> tuple[bool, int]:
            assert not_none(x[0].index)
            return x[0] not in new_post_set, x[0].index

        sorted_co = sorted(self.__pairs, key=sort_key)
        return self._co_sets(sorted_co, new_post_set)

    def _co_sets(self,
                 sorted_co: list[tuple[Condition, Condition]],
                 new: set[Condition],
                 allowed: set[Condition] | None = None,
                 constructed: list[Condition] | None = None,
                 current: int = 0) -> Generator[tuple[Condition, ...], None, None]:
        if constructed is None:
            constructed = []

        n = len(sorted_co)
        if current >= n:  # sorted_co закончился
            return

        if allowed is None and sorted_co[current][0] not in new:  # Ни одно из новых значений не добавлено
            # Значит все coset-ы в этой ветви уже учтены в pe
            return

            # Пропуск недопустимых значений
        if allowed is not None:
            while current < n and sorted_co[current][0] not in allowed:
                current += 1

        if current >= n:  # sorted_co закончился
            return

        el = sorted_co[current][0]

        current, new_allowed = self.create_new_allowed(allowed, current, el, n, sorted_co)
        constructed.append(el)
        yield tuple(constructed)

        constructed.append(el)
        yield tuple(constructed)

        yield from self._co_sets(sorted_co, new, new_allowed,
                                 constructed,
                                 current)

        constructed.pop()
        yield from self._co_sets(sorted_co, new, allowed, constructed, current)

    def create_new_allowed(self, allowed: set[Condition] | None, current: int, el: Condition, n: int,
                           sorted_co: list[tuple[Condition, Condition]]) -> tuple[int, set[Condition]]:
        new_allowed = set()
        while current < n and (pair := sorted_co[current])[0] == el:
            if allowed is None or pair[1] in allowed:
                new_allowed.add(pair[1])
            current += 1

        return current, new_allowed
