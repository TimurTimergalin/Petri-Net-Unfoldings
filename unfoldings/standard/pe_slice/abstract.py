from abc import ABC, abstractmethod
from typing import Iterable

from ..possible_extensions import PossibleExtensions, PossibleExtension
from ..settings import Settings


class PeSlicer(ABC):
    def __init__(self, settings: Settings):
        self._settings = settings

    @property
    def settings(self) -> Settings:
        return self._settings

    @abstractmethod
    def front(self, pe: PossibleExtensions) -> Iterable[PossibleExtension]:
        pass
