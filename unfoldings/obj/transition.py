from __future__ import annotations

from typing import Generator, Iterable, Self, Any

from ..typing_utils import *

from . import petri_net, place
from .arc import ArcPair


class Transition:
    """Класс перехода сети Петри. Переход может быть двух видов - привязанный и непривязанный. Привязанный переход
    уже находится в какой-то сети Петри. Хранит ссылку на сеть и индекс в ней.
    Непривязанный переход ещё не добавлен в сеть Петри, и содержит информацию, необходимую для его добавления -
    имя и дуги (все дуги должны вести к привязанным позициям).

    Аттрибуты:

    net -- сеть, к которой привязан переход, или None (в случае непривязанного перехода)

    ind -- индекс в сети, к которой привязан переход, или None (в случае непривязанного перехода)
        """

    def __init__(self, name: str | None = None, arcs: Iterable[tuple[place.Place, ArcPair]] | None = None) -> None:
        self.net: petri_net.PetriNet | None = None
        self.index: int | None = None
        self._name: str | None = name
        self._arcs: list[tuple[place.Place, ArcPair]] | None = list(arcs) if arcs is not None else None

    @classmethod
    def bound(cls, net: petri_net.PetriNet, index: int) -> Self:
        """Создает привязанный переход"""
        res = cls()
        res.net = net
        res.index = index
        res._name = None
        res._arcs = None
        return res

    @property
    def is_bound(self) -> bool:
        """True, если переход привязанный, False иначе"""
        return self.index is not None

    @property
    def name(self) -> str:
        """Имя перехода"""
        if self.is_bound:
            assert not_none(self.net)
            assert not_none(self.index)
            return self.net.t_names[self.index]

        assert not_none(self._name)
        return self._name

    @property
    def arcs(self) -> Generator[tuple[place.Place, ArcPair], None, None]:
        """Дуги перехода (входящие и исходящие)"""
        if self.is_bound:
            assert not_none(self.net)
            assert not_none(self.index)
            yield from self.net.transition_arcs(self.index)

        assert not_none(self._arcs)
        yield from self._arcs

    @property
    def preset(self) -> Generator[tuple[place.Place, int], None, None]:
        """Предшественники перехода (с весом)"""
        yield from ((p, ap.from_p_to_t) for p, ap in self.arcs if ap.from_p_to_t != 0)

    @property
    def postset(self) -> Generator[tuple[place.Place, int], None, None]:
        """Последователи перехода (с весом)"""
        yield from ((p, ap.from_t_to_p) for p, ap in self.arcs if ap.from_t_to_p != 0)

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
        if not isinstance(other, Transition):
            return False
        if self.is_bound is not other.is_bound:
            return False

        if self.is_bound:
            return self.net is other.net and self.index == other.index

        return self is other

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Transition({self.name})"
