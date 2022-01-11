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
