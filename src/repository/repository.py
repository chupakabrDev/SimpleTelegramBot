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
    def update_or_create(self, element: TElement) -> int:
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, key: int) -> Optional[TElement]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: int) -> Optional[TElement]:
        raise NotImplementedError

class InMemoryRepository(Repository[TElement]):
    def __init__(self, generated: bool = True):
        super().__init__(generated)
        self.counter = 0
        self.elements: dict[int, TElement] = {}

    def update_or_create(self, element: TElement) -> int:
        if element.key not in self.elements and self.generated:
            self.counter += 1
            element.key = self.counter

        self.elements[element.key] = element

        return element.key

    def retrieve(self, key: int) -> Optional[TElement]:
        element = self.elements.get(key)
        if element is not None:
            return copy.deepcopy(element)

        return None

    def delete(self, key: int) -> Optional[TElement]:
        return self.elements.pop(key, None)
