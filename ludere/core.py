from typing import List, Type, Set, Any, Dict, Optional, TypeVar

from ludere.reflection import resolve_constructor_parameter_types

T = TypeVar("T")


class Ludere:

    def __init__(self):
        self._pending_resolution: Set[Type] = set()
        self._resolved_beans: Dict[Type, Any] = {}

    def register(self, cls):
        self._pending_resolution.add(cls)
        return cls

    def resolve(self):
        while len(self._pending_resolution) > 0:
            for cls in list(self._pending_resolution):
                self._attempt_to_resolve(cls)

    def get_bean(self, cls: Type[T]) -> Optional[T]:
        return self._resolved_beans.get(cls)

    def _attempt_to_instantiate(self, cls: Type[T]) -> Optional[T]:
        constructor_dependencies = resolve_constructor_parameter_types(cls)

        if not all(self._is_resolved(dep_cls) for dep_cls in constructor_dependencies):
            return None

        constructor_arguments = [self.get_bean(dep_cls) for dep_cls in constructor_dependencies]
        return cls(*constructor_arguments)

    def _is_resolved(self, cls: Type):
        return cls in self._resolved_beans.keys()

    def _attempt_to_resolve(self, cls: Type):
        instance = self._attempt_to_instantiate(cls)

        if instance is None:
            return

        self._resolved_beans[cls] = instance
        self._pending_resolution.remove(cls)
