from typing import TypeVar, TypeGuard, Protocol, Any


T = TypeVar("T")


def not_none(value: T | None) -> TypeGuard[T]:
    return True  # Никаких проверок не делается - это лишь сообщение для компилятора


def to_not_none(value: T | None) -> T:
    assert not_none(value)
    return value


__all__ = ["not_none", "to_not_none"]
