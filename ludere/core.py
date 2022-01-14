from threading import Thread
from typing import List, Type, Set, Any, Dict, Optional, TypeVar, Callable

from ludere.reflection import resolve_constructor_parameter_types, resolve_function_parameter_types, has_return_type

T = TypeVar("T")


class Ludere:

    def __init__(self):
        self._pending_classes: Set[Type] = set()
        self._pending_bean_providers: List[Callable] = []
        self._pending_bean_modifiers: List[Callable] = []
        self._resolved_beans: Dict[Type, Any] = {}

    def register(self, cls):
        self._pending_classes.add(cls)
        return cls

    def register_function(self, f):
        if has_return_type(f):
            self._pending_bean_providers.append(f)
        else:
            self._pending_bean_modifiers.append(f)

    def resolve(self):
        while len(self._pending_classes) > 0 or len(self._pending_bean_providers) > 0:
            for cls in list(self._pending_classes):
                self._attempt_to_resolve_class(cls)

            for f in list(self._pending_bean_providers):
                self._attempt_to_resolve_function(f)

    def run_modifiers(self):
        for modifier in self._pending_bean_modifiers:
            dependencies = resolve_function_parameter_types(modifier)

            assert all(self._is_resolved(dep_cls) for dep_cls in dependencies)

            arguments = [self.get_bean(dep_cls) for dep_cls in dependencies]
            modifier(*arguments)

    def get_bean(self, cls: Type[T]) -> Optional[T]:
        for bean_cls, bean in self._resolved_beans.items():
            if issubclass(bean_cls, cls):
                return bean

    def run(self):
        self.resolve()
        self._run_on_start_hooks()

    def stop(self):
        self._run_on_stop_hooks()

    def _is_resolved(self, cls: Type):
        return cls in self._resolved_beans.keys()

    def _attempt_to_resolve_class(self, cls: Type):
        instance = self._attempt_to_instantiate_class(cls)

        if instance is None:
            return

        self._resolved_beans[cls] = instance
        self._pending_classes.remove(cls)

    def _attempt_to_instantiate_class(self, cls: Type[T]) -> Optional[T]:
        constructor_dependencies = resolve_constructor_parameter_types(cls)

        if not all(self._is_resolved(dep_cls) for dep_cls in constructor_dependencies):
            return None

        constructor_arguments = [self.get_bean(dep_cls) for dep_cls in constructor_dependencies]
        return cls(*constructor_arguments)

    def _attempt_to_resolve_function(self, f):
        instance = self._attempt_to_instantiate_function(f)

        if instance is None:
            return

        self._resolved_beans[type(instance)] = instance
        self._pending_bean_providers.remove(f)

    def _attempt_to_instantiate_function(self, f):
        dependencies = resolve_function_parameter_types(f)

        if not all(self._is_resolved(dep_cls) for dep_cls in dependencies):
            return None

        arguments = [self.get_bean(dep_cls) for dep_cls in dependencies]
        return f(*arguments)

    def _run_on_start_hooks(self):
        for bean in self._resolved_beans.values():
            if isinstance(bean, LifecycleHooks):
                Thread(target=bean.on_start).start()

    def _run_on_stop_hooks(self):
        for bean in self._resolved_beans.values():
            if isinstance(bean, LifecycleHooks):
                Thread(target=bean.on_stop).start()


class LifecycleHooks:

    def on_start(self):
        pass

    def on_stop(self):
        pass
