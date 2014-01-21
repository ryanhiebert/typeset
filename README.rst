TypeSet
=======

Using Types as Sets. This Python 3 only library allows you to use metaclass
magic to make types act like sets. For example::

    >>> from typeset import TypeSet
    >>> class Integer(int, metaclass=TypeSet):
    ...     pass
    ...
    >>> class Float(float, metaclass=TypeSet):
    ...     pass
    ...
    >>> Number = Integer | Float
    >>> three = Integer(3)
    >>> three_halves = Float(1.5)
    >>> three in Number and three_halves in Number
    True
