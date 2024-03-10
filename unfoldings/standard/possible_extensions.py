from typing import Callable

from ..prefix_obj import Condition
from ..prefix_obj import Event

PossibleExtension = tuple[Event, tuple[Condition, ...]]


def _left_child(ind: int) -> int:
    return 2 * ind + 1


def _right_child(ind: int) -> int:
    return 2 * ind + 2


def _parent(ind: int) -> int:
    return (ind - 1) // 2


class PossibleExtensions:
    def __init__(self, compare_function: Callable[[Event, Event], int]):
        self.compare_function = compare_function
        self.heap: list[PossibleExtension] = []

    def _in_bounds(self, ind: int) -> bool:
        return 0 <= ind < len(self.heap)

    def _heapify_down(self, ind: int) -> None:
        if not self._in_bounds(ind):
            return
        while True:
            li = _left_child(ind)
            ri = _right_child(ind)

            lv = self.heap[li][0] if self._in_bounds(li) else None
            rv = self.heap[ri][0] if self._in_bounds(ri) else None
            cv = self.heap[ind][0]

            if lv is not None and self.compare_function(cv, lv) > 0 and (
                    rv is None or self.compare_function(rv, lv) >= 0):
                self.heap[ind], self.heap[li] = self.heap[li], self.heap[ind]
                ind = li
            elif rv is not None and self.compare_function(cv, rv) > 0 and (
                    lv is None or self.compare_function(lv, rv) >= 0):
                self.heap[ind], self.heap[ri] = self.heap[ri], self.heap[ind]
                ind = ri
            else:
                break

    def _heapify_up(self, ind: int) -> None:
        if not self._in_bounds(ind):
            return
        while True:
            pi = _parent(ind)
            if not self._in_bounds(pi):
                break

            pv = self.heap[pi][0]
            cv = self.heap[ind][0]

            if self.compare_function(cv, pv) < 0:
                self.heap[ind], self.heap[pi] = self.heap[pi], self.heap[ind]
                ind = pi
            else:
                break

    def add(self, el: PossibleExtension) -> None:
        ni = len(self.heap)
        self.heap.append(el)
        self._heapify_up(ni)

    def pop(self) -> PossibleExtension:
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]

        r = self.heap.pop()
        self._heapify_down(0)
        return r

    def peak(self) -> PossibleExtension:
        return self.heap[0]

    def __len__(self) -> int:
        return len(self.heap)
