from typing import List, Type, Set, Any, Dict

from ludere.reflection import resolve_immediate_dependencies, resolve_dependency_graph


class Ludere:

    def __init__(self):
        self._registered_classes: List[Type] = []
        self._unresolved_dependencies: Set[Type] = set()
        self._resolved_dependencies: Dict[Type, Any] = {}

    def register(self, cls):
        self._registered_classes.append(cls)
        return cls

    def run(self):
        self._instantiate_registered_classes()

    def _instantiate_registered_classes(self):
        for cls in self._registered_classes:
            self._unresolved_dependencies.add(cls)
            self._unresolved_dependencies.update(resolve_dependency_graph(cls))

        for _pass in range(1, 10):
            print(f"DI pass {_pass}...")

            for cls in list(self._unresolved_dependencies):
                self._attempt_to_resolve(cls)

            if len(self._unresolved_dependencies) == 0:
                return

    def _can_be_instantiated(self, cls) -> bool:
        required_dependencies = set(resolve_immediate_dependencies(cls))
        return required_dependencies.issubset(self._resolved_dependencies.keys())

    def _attempt_to_resolve(self, cls):
        if not self._can_be_instantiated(cls):
            return

        instance = self._instantiate_with_dependencies(cls)
        self._resolved_dependencies[cls] = instance
        self._unresolved_dependencies.remove(cls)

    def _instantiate_with_dependencies(self, cls: Type):
        dependency_types = resolve_immediate_dependencies(cls)
        dependencies = [self._resolved_dependencies[cls] for cls in dependency_types]

        return cls(*dependencies)
