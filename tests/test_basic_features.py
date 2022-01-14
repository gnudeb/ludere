from dataclasses import dataclass

from ludere.core import Ludere


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
