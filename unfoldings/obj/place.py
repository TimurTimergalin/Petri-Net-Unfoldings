from __future__ import annotations

from ..typing_utils import *

from . import petri_net, transition
from .arc import ArcPair

from typing import Generator, Iterable, Self, Any


class Place:
    """Класс позиции сети Петри. Позиция может быть двух видов - привязанная и непривязанная. Привязанная позиция
    уже находится в какой-то сети Петри. Хранит ссылку на сеть и индекс в ней.
    Непривязанная позиция ещё не добавлена в сеть Петри, и содержит информацию, необходимую для ее добавления -
    имя и дуги (все дуги должны вести к привязанным переходам).

    Аттрибуты:

    net -- сеть, к которой привязана позиция, или None (в случае непривязанной позиции)

    ind -- индекс в сети, к которой привязана позиция, или None (в случае непривязанной позиции)
    """
    def __init__(self, name: str | None = None,
                 arcs: Iterable[tuple[transition.Transition, ArcPair]] | None = None) -> None:
        self.net: petri_net.PetriNet | None = None
        self.index: int | None = None
        self._name: str | None = name
        self._arcs: list[tuple[transition.Transition, ArcPair]] | None = list(arcs) if arcs is not None else None

    @classmethod
    def bound(cls, net: petri_net.PetriNet, index: int) -> Self:
        """Создает привязанную позицию"""
        res = cls()
        res.net = net
        res.index = index
        return res

    @property
    def is_bound(self) -> bool:
        """True, если позиция привязанная, False иначе"""
        return self.index is not None

    @property
    def name(self) -> str:
        """Имя позиции"""
        if self.is_bound:
            assert not_none(self.net)
            assert not_none(self.index)
            return self.net.p_names[self.index]

        assert not_none(self._name)
        return self._name

    @property
    def arcs(self) -> Generator[tuple[transition.Transition, ArcPair], None, None]:
        """Дуги позиции (входящие и исходящие)"""
        if self.is_bound:
            assert not_none(self.net)
            assert not_none(self.index)
            yield from self.net.place_arcs(self.index)
            return

        assert not_none(self._arcs)
        yield from self._arcs

    @property
    def preset(self) -> Generator[tuple[transition.Transition, int], None, None]:
        """Предшественники позиции (с весом)"""
        yield from ((t, ap.from_t_to_p) for t, ap in self.arcs if ap.from_t_to_p != 0)

    @property
    def postset(self) -> Generator[tuple[transition.Transition, int], None, None]:
        """Последователи позиции (с весом)"""
        yield from ((t, ap.from_p_to_t) for t, ap in self.arcs if ap.from_p_to_t != 0)

    def on_add(self, net: petri_net.PetriNet, index: int) -> None:
        self.net = net
        self.index = index
        self._name = None
        self._arcs = None

    def __hash__(self) -> int:
        if self.is_bound:
            return hash(self.index)

        return id(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Place):
            return False
        if self.is_bound is not other.is_bound:
            return False

        if self.is_bound:
            return self.net is other.net and self.index == other.index

        return self is other

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name})"
