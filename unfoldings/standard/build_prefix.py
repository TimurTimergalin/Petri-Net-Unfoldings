from itertools import chain
from typing import Callable, MutableSequence, MutableSet, cast

from .concurrency_relation import Co
from .pe_slice import PeSlicer
from .possible_extensions import PossibleExtensions, PossibleExtension
from .settings import Settings
from .update_possible_extensions import PeUpdater
from ..obj import PetriNet, Marking, Place, Transition, ArcPair
from ..prefix_obj import Prefix, Condition, Event

from multiprocessing import Pool
from multiprocessing.managers import SyncManager

from ..typing_utils import not_none


class PrefixManager(SyncManager):
    pass


def init() -> None:
    PrefixManager.register("set", set)


def parallel_update_pe(args: tuple[
    MutableSequence[PossibleExtension],
    PeUpdater,
    MutableSet[int],
    Settings,
    Event,
    Co,
    set[Place]]) -> None:
    pe_list, pe_updater, cutoff_set, settings, e, co, postset = args

    cond = settings.check_cutoff(e)

    if not cond:
        transitions = set(chain.from_iterable((y for y, _ in x.postset) for x in postset))
        pe_updater.update(e, transitions, co, pe_list)
    else:
        assert not_none(e.index)
        cutoff_set.add(e.index)


def build_prefix(net: PetriNet, m0: Marking, settings: Settings, slicer_factory: Callable[[Settings], PeSlicer],
                 process_count: int) -> Prefix:
    with PrefixManager() as manager:
        res = Prefix()
        co = Co()
        pe = PossibleExtensions(settings.compare_events)
        pe_update = PeUpdater()
        slicer = slicer_factory(settings)

        e = Event(arcs=[])

        res.add_transition(e)

        for p in m0.elements():
            c = Condition(label=p, arcs=[(e, ArcPair(0, 1))])
            res.add_place(c)

        co.update(e, set(res.places()))

        settings.check_and_update_cutoff(e)
        extensions: MutableSequence[PossibleExtension] = []
        pe_update.update(e, net.transitions(), co, extensions)
        for extension in extensions:
            pe.add(extension)

        while pe:
            sl = slicer.front(pe)

            postsets: list[set[Place]] = []

            for e, pre in sl:
                res.add_transition(e)
                postset: set[Place] = set()

                for p, w in e.label.postset:
                    postset.add(p)
                    for _ in range(w):
                        c = Condition(label=p, arcs=[(e, ArcPair(0, 1))])
                        res.add_place(c)

                postsets.append(postset)
                co.update(e, set(res.places()))

            extensions = manager.list()
            cutoffs = manager.set()  # type: ignore

            with Pool(process_count) as pool:
                pool.map(parallel_update_pe,
                         [(extensions, pe_update,
                           cutoffs, settings, ev, co, st) for (ev, _), st in zip(sl, postsets)])

            for extension in extensions:
                extension[0].label.net = net  # При передаче процессу сеть копируется, а ссылка на оригинал теряется
                pe.add(extension)

            for e, _ in sl:
                if not cutoffs.issuperset({e.index}):
                    settings.update_cutoff(e)

        return res
