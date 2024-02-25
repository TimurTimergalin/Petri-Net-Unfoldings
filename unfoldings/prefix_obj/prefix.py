from ..obj import PetriNet, Place, Transition


class Prefix(PetriNet):
    """Класс префикса развертки сети Петри

    Новые аттрибуты:

    c_labels -- массив мест, которыми помечены условия развертки

    e_labels -- массив переходов, которыми помечены события развертки
    """
    def __init__(self) -> None:
        super().__init__()
        self.c_labels: list[Place] = []
        self.e_labels: list[Transition] = []
