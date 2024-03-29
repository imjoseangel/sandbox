import unittest

from code import add


class TestAddFunctions(unittest.TestCase):
    def test_add_integers(self):
        result = add(1, 2)
        self.assertEqual(result, 3)


if __name__ == "__main__":
    unittest.main()
