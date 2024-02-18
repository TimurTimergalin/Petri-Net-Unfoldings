"""
В этом файле представлены функции для преобразования pm4py-представление сетей Петри в наше представление и наоборот
"""
from __future__ import annotations

from pm4py.objects.petri_net.obj import PetriNet as Pm4PyNet, Marking as Pm4PyMarking
from pm4py.objects.petri_net.utils import petri_utils

from .petri_net import PetriNet
from .marking import Marking
from .arc import ArcPair
from .place import Place


def from_pm4py(net: Pm4PyNet, *markings: Pm4PyMarking) -> tuple[PetriNet, list[Marking]]:
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
    return res_net, res_markings


def to_pm4py(net: PetriNet,
             *markings: Marking,
             net_name: str | None = None) -> tuple[Pm4PyNet, list[Pm4PyMarking]]:
    places = {i: Pm4PyNet.Place(name) for i, name in enumerate(net.p_names)}
    transitions = {i: Pm4PyNet.Transition(name, label=name) for i, name in enumerate(net.t_names)}

    res_net = Pm4PyNet(net_name or "")
    for p in places.values():
        res_net.places.add(p)

    for t in transitions.values():
        res_net.transitions.add(t)

    for i in places:
        for j in transitions:
            arc = net[i, j]

            if arc.from_p_to_t != 0:
                petri_utils.add_arc_from_to(places[i], transitions[j], res_net, arc.from_p_to_t)

            if arc.from_t_to_p != 0:
                petri_utils.add_arc_from_to(transitions[j], places[i], res_net, arc.from_t_to_p)

    res_markings = [
        Pm4PyMarking({places[k.index]: v for k, v in marking.items()})
        for marking in markings
    ]

    return res_net, res_markings
