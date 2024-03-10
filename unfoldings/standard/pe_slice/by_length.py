from typing import Iterable, cast

from .abstract import PeSlicer
from ..possible_extensions import PossibleExtensions, PossibleExtension
from ..settings import Settings
from ..settings import LengthSettings


class LengthSlicer(PeSlicer):
    def __init__(self, settings: Settings):
        assert isinstance(settings, LengthSettings)
        super().__init__(settings)

    @property
    def settings(self) -> LengthSettings:
        return cast(LengthSettings, super().settings)

    def front(self, pe: PossibleExtensions) -> Iterable[PossibleExtension]:
        el = pe.pop()
        res = [el]

        while self.settings.configuration_length(pe.peak()[0]) == self.settings.configuration_length(el[0]):
            res.append(pe.pop())

        return res
