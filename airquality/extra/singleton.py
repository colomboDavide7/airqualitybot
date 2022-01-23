# ======================================
# @author:  Davide Colombo
# @date:    2022-01-23, dom, 11:23
# ======================================


class Singleton(type):
    """
    A class that inherits from *type* built-in class (a.k.a., a metaclass, a class for creating a class).

    This class overrides the __call__ dunder method for controlling the creation of the concrete class for which
    this metaclass will be used.

    This is an implementation of the Singleton design pattern.

    foo_metaclass = Singleton('Foo', (), {})    # define an instance of the metaclass that can create 'Foo' instances.
    foo_instance = foo_metaclass()              # call __call__ method of the metaclass and return an instance of 'Foo'.

    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
