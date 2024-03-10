from abc import ABC

from ....prefix_obj import Event
from ....obj import Marking
from ..abstract import Settings


class BasicCutoffDetection(Settings, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.min_by_mark: dict[Marking, Event] = {}

    def check_cutoff(self, event: Event) -> bool:
        mark = self.create_config(event).mark()
        return not (mark not in self.min_by_mark or self.compare_events(event, self.min_by_mark[mark]) <= 0)

    def update_cutoff(self, event: Event) -> None:
        mark = self.create_config(event).mark()
        self.min_by_mark[mark] = event

    def check_and_update_cutoff(self, event: Event) -> bool:
        mark = self.create_config(event).mark()
        if mark not in self.min_by_mark or self.compare_events(event, self.min_by_mark[mark]) <= 0:
            self.min_by_mark[mark] = event
            return False
        return True
