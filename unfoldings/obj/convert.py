"""
В этом файле представлены функции для преобразования pm4py-представления сетей Петри в наше представление и наоборот
"""
from __future__ import annotations

from ..typing_utils import *

from pm4py.objects.petri_net.obj import PetriNet as Pm4PyNet, Marking as Pm4PyMarking
from pm4py.objects.petri_net.utils import petri_utils

from .petri_net import PetriNet
from .marking import Marking
from .arc import ArcPair
from .place import Place

from typing import cast


def net_from_pm4py(net: Pm4PyNet,
                   *markings: Pm4PyMarking
                   ) -> tuple[PetriNet, list[Marking], dict[Pm4PyNet.Place, int], dict[Pm4PyNet.Transition, int]]:
    """Преобразует pm4py-представление сети Петри в наше представление. Дополнительно преобразует все переданные
    разметки.

    Возвращает новое представление сети и разметок, а также индексы позиций и переходов в новом представлении
    """
    places = {p: ind for ind, p in enumerate(sorted(net.places, key=lambda p: p.name))}
    transitions = {t: ind for ind, t in enumerate(sorted(net.transitions, key=lambda t: t.name))}

    matrix = []

    for _ in places:
        matrix.append([ArcPair.no() for _ in transitions])

    for a in net.arcs:
        f, s, w = a.source, a.target, a.weight

        if isinstance(f, Pm4PyNet.Place):
            prev = matrix[places[f]][transitions[s]]
            new = ArcPair(w, prev.from_t_to_p)
            matrix[places[f]][transitions[s]] = new
        else:
            prev = matrix[places[s]][transitions[f]]
            new = ArcPair(prev.from_p_to_t, w)
            matrix[places[s]][transitions[f]] = new

    res_net = PetriNet()
    res_net.adjacency_matrix = matrix
    res_net.p_names = [p.name for p in places]
    res_net.t_names = [t.name for t in transitions]

    res_markings = [
        Marking({Place.bound(res_net, places[k]): v for k, v in marking.items()})
        for marking in markings
    ]
    return res_net, res_markings, places, transitions


def net_to_pm4py(net: PetriNet,
                 *markings: Marking,
                 net_name: str | None = None) -> tuple[Pm4PyNet, list[Pm4PyMarking], list[Pm4PyNet.Place], list[Pm4PyNet.Transition]]:
    """Преобразует наше представление сети Петри в pm4py-представление. Дополнительно преобразует все переданные
    разметки.

    Возвращает новое представление сети и разметок, а также pm4py-представление всех мест и переходов сети (по индексам)
    """
    places = [Pm4PyNet.Place(name) for name in net.p_names]
    transitions = [Pm4PyNet.Transition(name, label=name) for name in net.t_names]

    res_net = Pm4PyNet(net_name or "")
    for p in places:
        cast(set[Pm4PyNet.Place], res_net.places).add(p)

    for t in transitions:
        cast(set[Pm4PyNet.Transition], res_net.transitions).add(t)

    for i, p in enumerate(places):
        for j, t in enumerate(transitions):
            arc = net[i, j]

            if arc.from_p_to_t != 0:
                petri_utils.add_arc_from_to(p, t, res_net, arc.from_p_to_t)

            if arc.from_t_to_p != 0:
                petri_utils.add_arc_from_to(t, p, res_net, arc.from_t_to_p)

    res_markings = [
        Pm4PyMarking({places[to_not_none(k.index)]: v for k, v in marking.items()})
        for marking in markings
    ]

    return res_net, res_markings, places, transitions
