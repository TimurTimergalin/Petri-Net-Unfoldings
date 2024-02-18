from pm4py.objects.petri_net.obj import PetriNet as Pm4PyNet

from .prefix import Prefix
from .. import obj


def to_pm4py(prefix: Prefix,
             net_name: str | None = None
             ) -> \
             tuple[Pm4PyNet, dict[Pm4PyNet.Place, dict[str, str]], list[Pm4PyNet.Place], list[Pm4PyNet.Transition]]:
    """Преобразовывает наше представление префикса развертки в pm4py-представление.

    Возвращает новое представление префикса развертки, decorations для pm4py.view_petri_net,
    а также pm4py-представление всех условий и событий префикса (по индексам)
    """
    pm_prefix, _, conditions, events = \
        obj.to_pm4py(prefix, net_name="Prefix" if net_name is None else f"Prefix of '{net_name}'")

    for i, t in enumerate(events):
        t.label = prefix.e_labels[i].name

    condition_decorations = {
        pm_place: {"label": prefix.c_labels[i].name}
        for i, pm_place in enumerate(conditions)
    }

    return pm_prefix, condition_decorations, conditions, events
