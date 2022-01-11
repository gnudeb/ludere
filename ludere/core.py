from typing import List, Type, Set, Any, Dict, Optional, TypeVar


T = TypeVar("T")


class Ludere:

    def __init__(self):
        self._pending_resolution: Set[Type] = set()
        self._resolved_beans: Dict[Type, Any] = {}

    def register(self, cls):
        self._pending_resolution.add(cls)
        return cls

    def resolve(self):
        for cls in list(self._pending_resolution):
            instance = cls()
            self._resolved_beans[cls] = instance
            self._pending_resolution.remove(cls)

    def get_bean(self, cls: Type[T]) -> Optional[T]:
        return self._resolved_beans.get(cls)
