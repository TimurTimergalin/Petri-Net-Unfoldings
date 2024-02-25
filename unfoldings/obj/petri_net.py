from __future__ import annotations

from ..typing_utils import *

from . import place, transition
from .arc import ArcPair

from itertools import chain
from typing import Generator, overload


class PetriNet:
    """Класс сети Петри

    Аттрибуты:

    adjacency_matrix -- матрица для хранения дуг между элементами сети. Индексам i, j соответствует запись
    ArcPair о дугах между i-ой позицией и j-м переходом

    p_names -- массив имен позиций

    t_names -- массив имен переходов
    """

    def __init__(self) -> None:
        self.adjacency_matrix: list[list[ArcPair]] = []
        self.p_names: list[str] = []
        self.t_names: list[str] = []

    @property
    def p_count(self) -> int:
        """Количество позиций в сети"""
        return len(self.p_names)

    @property
    def t_count(self) -> int:
        """Количество переходов в сети"""
        return len(self.t_names)

    def add_place(self, p: place.Place) -> None:
        """Добавляет новую позицию в сеть"""
        assert not p.is_bound, "such place already exists"
        self.p_names.append(p.name)

        row = [ArcPair.no()] * self.t_count
        self.adjacency_matrix.append(row)
        for t, ws in p.arcs:
            assert t.is_bound, "unknown transition"
            assert not_none(t.index)
            row[t.index] = ws

        p.on_add(self, self.p_count - 1)

    def add_transition(self, t: transition.Transition) -> None:
        """Добавляет новый переход в сеть"""
        assert not t.is_bound, "such transition already exists"
        self.t_names.append(t.name)

        for p, ws in t.arcs:
            assert p.is_bound, "unknown place"
            assert not_none(p.index)
            self.adjacency_matrix[p.index].append(ws)

        for row in self.adjacency_matrix:
            if len(row) != self.t_count:
                row.append(ArcPair.no())

        t.on_add(self, self.t_count - 1)

    def place_arcs(self, place_index: int) -> Generator[tuple[transition.Transition, ArcPair], None, None]:
        """Перечисляет все дуги между данной позицией и всеми переходами"""
        assert 0 <= place_index < self.p_count, "invalid place index"

        for ti, ap in enumerate(self.adjacency_matrix[place_index]):
            if ap == ArcPair.no():
                continue
            yield transition.Transition.bound(self, ti), ap

    def transition_arcs(self, transition_index: int) -> Generator[tuple[place.Place, ArcPair], None, None]:
        """Перечисляет все дуги между данным переходом и всеми позициями"""
        assert 0 <= transition_index < self.t_count, "invalid transition index"

        for pi, row in enumerate(self.adjacency_matrix):
            ap = row[transition_index]
            if ap == ArcPair.no():
                continue
            yield place.Place.bound(self, pi), ap

    @overload
    def __getitem__(self, item: int) -> list[ArcPair]:
        ...

    @overload
    def __getitem__(self, item: tuple[int, int]) -> ArcPair:
        ...

    def __getitem__(self, item: int | tuple[int, int]) -> list[ArcPair] | ArcPair:
        if isinstance(item, int):
            return self.adjacency_matrix[item]

        return self.adjacency_matrix[item[0]][item[1]]

    def __repr__(self) -> str:
        return f"PetriNet({self.adjacency_matrix})"

    def __str__(self) -> str:
        max_pt = max(
            len(f"pt: {a.from_p_to_t}" if a.from_p_to_t else "") for a in chain.from_iterable(self.adjacency_matrix))

        max_tp = max(
            len(f"tp: {a.from_t_to_p}" if a.from_t_to_p else "") for a in chain.from_iterable(self.adjacency_matrix))

        max_t_name = max(len(name) for name in self.t_names)
        max_column = max(max_t_name, max_pt + max_tp + 1)
        max_p_name = max(len(name) for name in self.p_names)

        header = "|" + "#" * max_p_name + "|" + "|".join(name.ljust(max_column) for name in self.t_names)
        lines = [
            "|" + p_name.rjust(max_p_name) + "|" +
            "|".join(
                (f"pt: {a.from_p_to_t}" if a.from_p_to_t else "").ljust(max_pt) +
                " " +
                (f"tp: {a.from_t_to_p}" if a.from_t_to_p else "").ljust(max_tp)
                for a in row
            )
            for p_name, row in zip(self.p_names, self.adjacency_matrix)
        ]

        return header + "|\n" + "|\n".join(lines) + "|"
