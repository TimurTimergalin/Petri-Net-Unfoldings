from __future__ import annotations

from typing import Iterable, Generator, cast

from .. import PetriNet
from ..typing_utils import *

from . import event, prefix
from ..obj import ArcPair, Place


class Condition(Place):
    """Класс условия развертки"""

    def __init__(self,
                 name: str | None = None,
                 label: Place | None = None,
                 arcs: Iterable[tuple[event.Event, ArcPair]] | None = None) -> None:
        super().__init__(name, arcs)
        self.net: prefix.Prefix | None = None
        self._label = label

    @property
    def label(self) -> Place:
        """Место, которым помечено условие"""
        if self.is_bound:
            assert not_none(self.net)
            assert not_none(self.index)
            return self.net.c_labels[self.index]

        assert not_none(self._label)
        return self._label

    def on_add(self, net: PetriNet, index: int) -> None:
        assert isinstance(net, prefix.Prefix)
        assert not_none(self._label)
        super().on_add(net, index)
        net.c_labels[index] = self._label

    @property
    def preset(self) -> Generator[tuple[event.Event, int], None, None]:
        for x, c in super().preset:
            yield cast(event.Event, x), c

    @property
    def postset(self) -> Generator[tuple[event.Event, int], None, None]:
        for x, c in super().postset:
            yield cast(event.Event, x), c
