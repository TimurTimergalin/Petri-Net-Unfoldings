from __future__ import annotations

from typing import NamedTuple


class ArcPair(NamedTuple):
    """Запись в таблице смежности сети Петри

    Аттрибуты:

    from_p_to_t -- вес дуги от позиции к переходу - неотрицательное целое число (если 0, то дуги нет)

    from_t_to_p -- все дуги от перехода к позиции - неотрицательное целое число (если 0, то дуги нет)
    """
    from_p_to_t: int
    from_t_to_p: int

    @classmethod
    def no(cls) -> ArcPair:
        """Возвращает ArcPair(0, 0)"""
        return ArcPair(0, 0)
