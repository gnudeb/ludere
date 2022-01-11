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
