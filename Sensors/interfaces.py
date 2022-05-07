from abc import ABC, abstractmethod


class Openable(ABC):
    @abstractmethod
    def open(self):
        ...

    @abstractmethod
    def close(self):
        ...

    @abstractmethod
    def get_is_open(self) -> bool:
        ...


class Turnable(ABC):
    @abstractmethod
    def turn_on(self):
        ...

    @abstractmethod
    def turn_off(self):
        ...

    @abstractmethod
    def get_is_turn_on(self) -> bool:
        ...
