from typing import Iterable, MutableSequence

from .concurrency_relation import Co
from .possible_extensions import PossibleExtension
from ..obj import ArcPair
from ..prefix_obj import Event
from ..obj import Transition, Marking
from ..typing_utils import not_none, to_not_none


class PeUpdater:
    def update(self, new: Event, transitions: Iterable[Transition], co: Co,
               pe_list: MutableSequence[PossibleExtension]) -> None:
        for coset in co.new_co_sets(new):
            assert not_none(new.index)
            if new.index < max(-1 if c.input is None else to_not_none(c.input.index) for c in coset):
                continue
            m = Marking(c.label for c in coset)
            for t in transitions:
                if self.is_enabled(t, m):
                    e = Event(label=t, arcs=[(c, ArcPair(1, 0)) for c in coset])
                    pe_list.append((e, coset))

    def is_enabled(self, t: Transition, m: Marking) -> bool:
        return all(m[c] == w for c, w in t.preset)
