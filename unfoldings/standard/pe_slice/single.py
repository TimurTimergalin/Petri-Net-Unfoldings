from .abstract import PeSlicer
from ..possible_extensions import PossibleExtensions, PossibleExtension


class SingleSlicer(PeSlicer):
    def front(self, pe: PossibleExtensions) -> tuple[PossibleExtension]:
        return pe.pop(),
