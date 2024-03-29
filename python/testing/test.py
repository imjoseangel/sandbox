# Make sure we have imported the unittest module
import unittest

# Import the code we need to test
from code import add

# Create a class that inherits from TestCase. This is necessary for
# unittest to detect it as a test, and to provide methods like
# self.assertEqual


class TestAddFunction(unittest.TestCase):

    # Write the test. It must be a method of a TestCase type
    # and the name MUST start with "test" to be detected
    def test_add_integers(self):

        # Write an assertion. Assertions are lines of code
        # that state what we expect to happen if everything
        # goes as planned.
        result = add(1, 2)
        self.assertEqual(result, 3)


# If this file is run (but not if it's imported),
# collect the tests and execute them.
if __name__ == "__main__":
    unittest.main()
