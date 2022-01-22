from dataclasses import dataclass

import pytest

from ludere.core import Ludere, LifecycleHooks, ResolutionError


def test_can_create_new_ludere():
    Ludere()


def test_can_instantiate_class_without_dependencies():
    ludere = Ludere()

    @ludere.register
    class SimpleClass:
        pass

    ludere.resolve()

    instance = ludere.get_bean(SimpleClass)
    assert type(instance) == SimpleClass


def test_can_instantiate_nested_dependency():
    ludere = Ludere()

    @ludere.register
    class Child:
        pass

    @ludere.register
    @dataclass
    class Parent:
        child: Child

    ludere.resolve()

    assert ludere.get_bean(Child) is not None
    assert ludere.get_bean(Parent) is not None
    assert type(ludere.get_bean(Parent).child) is Child


def test_can_instantiate_bean_from_provider():
    ludere = Ludere()

    class Bean:
        pass

    @ludere.register_function
    def bean_provider() -> Bean:
        return Bean()

    ludere.resolve()

    assert ludere.get_bean(Bean) is not None


def test_can_inject_beans_into_provider():
    ludere = Ludere()

    @ludere.register
    class Child:
        pass

    @dataclass
    class Parent:
        child: Child

    @ludere.register_function
    def bean_provider(child: Child) -> Parent:
        return Parent(child)

    ludere.resolve()

    assert ludere.get_bean(Child) is not None
    assert ludere.get_bean(Parent) is not None
    assert type(ludere.get_bean(Parent).child) is Child


def test_can_resolve_a_subclass():
    ludere = Ludere()

    class A:
        pass

    @ludere.register
    class B(A):
        pass

    ludere.resolve()

    assert type(ludere.get_bean(A)) == B
    assert id(ludere.get_bean(A)) == id(ludere.get_bean(B))


def test_two_classes_can_resolve_to_single_bean():
    ludere = Ludere()

    class A:
        pass

    class B:
        pass

    @ludere.register
    class AB(A, B):
        pass

    ludere.resolve()

    assert ludere.get_bean(A) is not None
    assert id(ludere.get_bean(A)) == id(ludere.get_bean(B)) == id(ludere.get_bean(AB))


def test_can_register_configuration_function():
    ludere = Ludere()

    @ludere.register
    @dataclass
    class ImportantObject:
        value: int = 5

    @ludere.register_function
    def configure_important_object(io: ImportantObject):
        io.value = 500

    ludere.run()

    assert ludere.get_bean(ImportantObject).value == 500


def test_bean_can_implement_on_start_lifecycle_hook():
    ludere = Ludere()

    @ludere.register
    @dataclass
    class Runner(LifecycleHooks):
        state: str = "not started"

        def on_start(self):
            self.state = "started"

    ludere.run()

    assert ludere.get_bean(Runner).state == "started"


def test_bean_can_implement_on_stop_lifecycle_hook():
    ludere = Ludere()

    @ludere.register
    @dataclass
    class Runner(LifecycleHooks):
        state: str = "running"

        def on_stop(self):
            self.state = "stopped"

    ludere.run()
    runner = ludere.get_bean(Runner)
    assert runner.state == "running"
    ludere.stop()
    assert runner.state == "stopped"


def test_attempt_to_resolve_nonexistent_class_dependency_fails():
    ludere = Ludere()

    class Child:
        pass

    @ludere.register
    @dataclass
    class Parent:
        child: Child

    @ludere.register_function
    def make_parent(child: Child) -> Parent:
        return Parent(child)

    with pytest.raises(ResolutionError):
        ludere.resolve()


def test_attempt_to_resolve_nonexistent_function_dependency_fails():
    ludere = Ludere()

    class Child:
        pass

    @dataclass
    class Parent:
        child: Child

    @ludere.register_function
    def make_parent(child: Child) -> Parent:
        return Parent(child)

    with pytest.raises(ResolutionError) as e:
        ludere.resolve()
