import copy
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

class Keyable:

    _key: int = -1

    @property
    def key(self) -> int:
        return self._key

    @key.setter
    def key(self, key: int):
        self._key = key

TElement = TypeVar('TElement', bound='Keyable')

class Repository(ABC, Generic[TElement]):

    def __init__(self, generated: bool = True):
        self.generated = generated

    @abstractmethod
    def query(self, start: int = 0, end: int = -1) -> list[TElement]:
        raise NotImplementedError

    @abstractmethod
    def update_or_create(self, element: TElement) -> int:
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, key: int) -> Optional[TElement]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: int) -> Optional[TElement]:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError


class InMemoryRepository(Repository[TElement]):
    def __init__(self, generated: bool = True):
        super().__init__(generated)
        self.counter = 0
        self.elements: dict[int, TElement] = {}

    def query(self, start: int = 0, end: int = -1) -> list[TElement]:
        if end == -1:
            selected = [k for k in self.elements if k >= start]
        else:
            if end < start:
                return []
            selected = [k for k in self.elements if start <= k <= end]

        return [copy.deepcopy(self.elements[k]) for k in selected]

    def update_or_create(self, element: TElement) -> int:
        if element.key not in self.elements and self.generated:
            element.key = self.counter
            self.counter += 1

        self.elements[element.key] = element

        return element.key

    def retrieve(self, key: int) -> Optional[TElement]:
        element = self.elements.get(key)
        if element is not None:
            return copy.deepcopy(element)

        return None

    def delete(self, key: int) -> Optional[TElement]:
        return self.elements.pop(key, None)

    def count(self) -> int:
        return len(self.elements)