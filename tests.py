import unittest
from typeset import TypeSet


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
        self.assertTrue(A.intersect(A) == A)
        self.assertTrue(A.union(A) == A)

if __name__ == '__main__':
    unittest.main()
