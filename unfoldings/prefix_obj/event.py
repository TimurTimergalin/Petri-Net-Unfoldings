from __future__ import annotations

from typing import Iterable, Generator, cast, Any

from ..typing_utils import *

from . import condition, prefix
from ..obj import ArcPair, Transition, PetriNet


class Event(Transition):
    """Класс события развертки"""

    def __init__(self,
                 name: str | None = None,
                 label: Transition | None = None,
                 arcs: Iterable[tuple[condition.Condition, ArcPair]] | None = None) -> None:
        super().__init__(name, arcs)
        self.net: prefix.Prefix | None = None
        self._label = label

    @property
    def label(self) -> Transition:
        """Переход, которым помечено условие"""
        if self.is_bound:
            assert not_none(self.net)
            assert not_none(self.index)
            return self.net.e_labels[self.index]

        assert not_none(self._label)
        return self._label

    @property
    def comparable_label(self) -> Any:
        """Ключ для сравнения переходов, которыми помечены события"""
        return self.label.index

    def on_add(self, net: PetriNet, index: int) -> None:
        assert isinstance(net, prefix.Prefix)
        assert not_none(self._label)
        super().on_add(net, index)
        net.e_labels.append(self._label)

    @property
    def preset(self) -> Generator[tuple[condition.Condition, int], None, None]:
        for x, c in super().preset:
            yield cast(condition.Condition, x), c

    @property
    def postset(self) -> Generator[tuple[condition.Condition, int], None, None]:
        for x, c in super().postset:
            yield cast(condition.Condition, x), c
