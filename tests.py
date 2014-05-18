import unittest
from typeset import PredicateSet, TypeSet


class PredicateSetTestCase(unittest.TestCase):
    def test_contains(self):
        int_set = PredicateSet(lambda x: isinstance(x, int))
        self.assertTrue(all(x in int_set for x in range(-10, 10)))

    def test_difference(self):
        a = PredicateSet(lambda x: x in set(range(2)))
        b = PredicateSet(lambda x: x in set(range(1, 3)))

        self.assertIn(0, a.difference(b))
        self.assertNotIn(1, a.difference(b))
        self.assertNotIn(2, a.difference(b))

        self.assertIn(0, a - b)
        self.assertNotIn(1, a - b)
        self.assertNotIn(2, a - b)

    def test_intersection(self):
        a = PredicateSet(lambda x: x in set(range(2)))
        b = PredicateSet(lambda x: x in set(range(1, 3)))

        self.assertNotIn(0, a.intersection(b))
        self.assertIn(1, a.intersection(b))
        self.assertNotIn(2, a.intersection(b))

        self.assertNotIn(0, a & b)
        self.assertIn(1, a & b)
        self.assertNotIn(2, a & b)

    def test_symmetric_difference(self):
        a = PredicateSet(lambda x: x in set(range(2)))
        b = PredicateSet(lambda x: x in set(range(1, 3)))

        self.assertIn(0, a.symmetric_difference(b))
        self.assertNotIn(1, a.symmetric_difference(b))
        self.assertIn(2, a .symmetric_difference(b))

        self.assertIn(0, a ^ b)
        self.assertNotIn(1, a ^ b)
        self.assertIn(2, a ^ b)

    def test_union(self):
        a = PredicateSet(lambda x: x in set(range(2)))
        b = PredicateSet(lambda x: x in set(range(1, 3)))

        self.assertIn(0, a.union(b))
        self.assertIn(1, a.union(b))
        self.assertIn(2, a.union(b))

        self.assertIn(0, a | b)
        self.assertIn(1, a | b)
        self.assertIn(2, a | b)


class TypeSetTestCase(unittest.TestCase):
    def test_instantiation(self):
        class A(metaclass=TypeSet):
            pass
        self.assertTrue(isinstance(A(), A))

    def test_self_intersect_union(self):
        class A(metaclass=TypeSet):
            pass
        self.assertTrue(A & A == A)
        self.assertTrue(A | A == A)
        self.assertTrue(A.intersection(A) == A)
        self.assertTrue(A.union(A) == A)

if __name__ == '__main__':
    unittest.main()
