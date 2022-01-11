import inspect
from dataclasses import dataclass, field
from typing import Set, Type, List


@dataclass
class DependencyTraverser:
    visited_types: Set[Type] = field(default_factory=set, init=False)

    def traverse(self, cls: Type) -> Set[Type]:
        deps = resolve_immediate_dependencies(cls)
        self.visited_types.update(deps)

        for dependency in deps:
            self.traverse(dependency)

        return set(self.visited_types)


def resolve_immediate_dependencies(cls: Type) -> List[Type]:
    signature = inspect.signature(cls.__init__)
    parameters = dict(signature.parameters)
    parameters.pop("self")
    required_parameters = [p for n, p in parameters.items() if p.default is inspect.Parameter.empty]
    types = [p.annotation for p in required_parameters]

    return types


def resolve_dependency_graph(cls: Type) -> Set[Type]:
    traverser = DependencyTraverser()
    return traverser.traverse(cls)
