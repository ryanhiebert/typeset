class PredicateSet:
    def __init__(self, predicate):
        self.predicate = predicate

    def __contains__(self, item):
        return self.predicate(item)

    def isdisjoint(self, other):
        return not (other in self or self in other)

    def difference(self, other):
        if self is other:
            return set()
        else:
            return PredicateSet(lambda x: x in self and x not in other)

    def intersection(self, other):
        if self is other:
            return self
        else:
            return PredicateSet(lambda x: x in self and x in other)

    def symmetric_difference(self, other):
        left = self.difference(other)
        right = other.difference(self)
        if not left and not right:
            return set()
        else:
            return PredicateSet(lambda x: x in left or x in right)

    def union(self, other):
        if self is other:
            return self
        else:
            return PredicateSet(lambda x: x in self or x in other)

    __and__ = __rand__ = __iand__ = intersection
    __or__ = __ror__ = __ior__ = union
    __sub__ = __rsub__ = __isub__ = difference
    __xor__ = __rxor__ = __ixor__ = symmetric_difference


class TypeSet(type):
    def __init__(self, name, bases, dict):
        self.__composition = self

    def __repr__(self):
        return type.__repr__(self).replace("<class ", "<TypeSet ")

    @classmethod
    def __compose(cls, self, other, method):
        if not isinstance(self, TypeSet) or not isinstance(other, TypeSet):
            raise ValueError('Both arguments must have metaclass TypeSet')
        if method not in ('&', '|', '-', '^'):
            raise ValueError('method must be one of "{}"'.format('&|-^'))
        if self is other and method in ('&', '|'):
            return self

        class new(self, other, metaclass=cls):
            pass

        new.__name__ = '({} {} {})'.format(
            self.__name__, method, other.__name__)
        # Stored in infix notation
        new.__composition = (self.__composition, method, other.__composition)
        return new

    def __instancecheck__(self, instance):
        print('In instancecheck')
        if isinstance(self.__composition, TypeSet):
            print('Raw Instance')
            print('type says {}'.format(type.__instancecheck__(self, instance)))
            return type.__instancecheck__(self, instance)

        left, method, right = self.__composition
        if method == '&':
            return (isinstance(instance, left) and
                    isinstance(instance, right))
        elif method == '|':
            return (isinstance(instance, left) or
                    isinstance(instance, right))
        elif method == '-':
            return (isinstance(instance, left) and
                    not isinstance(instance, right))
        elif method == '^':
            isleft = isinstance(instance, left)
            isright = isinstance(instance, right)
            return isleft and not isright or not isleft and isright

        raise RuntimeError('Could not determine if an instance')

    def __subclasscheck__(self, subclass):
        if subclass is self:
            return True
        if isinstance(subclass.__composition, TypeSet):
            return False

        left, method, right = self.__composition
        ### FIX THE OR ISSUE (A | A -> A)
        if method in ('|', '^'):
            return False
        elif method == '&':
            return issubclass(subclass, left) or issubclass(subclass, right)
        elif method == '-':
            return (issubclass(subclass, left) and
                    not issubclass(subclass, right))

        raise RuntimeError('Could not determine if a subclass')

    def copy(self):
        raise NotImplementedError

    def issubset(self, other):
        return issubclass(self, other)

    def issuperset(self, other):
        return issubclass(other, self)

    def isdisjoint(self, other):
        return not (self.issubset(self, other) or self.issuperset(self, other))

    def difference(self, other):
        return self.__compose(self, other, '-')

    def intersection(self, other):
        return self.__compose(self, other, '&')

    def symmetric_difference(self, other):
        return self.__compose(self, other, '^')

    def union(self, other):
        return self.__compose(self, other, '|')

    def __contains__(self, item):
        return isinstance(item, self)

    __and__ = __rand__ = __iand__ = intersection
    __or__ = __ror__ = __ior__ = union
    __sub__ = __rsub__ = __isub__ = difference
    __xor__ = __rxor__ = __ixor__ = symmetric_difference

    def __call__(self, *args, **kwargs):
        if isinstance(self.__composition, TypeSet):
            return type.__call__(self, *args, **kwargs)
        raise NotImplementedError

    def __iter__(self):
        return NotImplemented

    def __len__(self):
        return NotImplemented
