# django unit test framework looks for files beginning with tests
# and use it for testing


from django.test import TestCase   # testcase is a class that comes with django
# with helper function that helps to test code
from app.calc import add, subtract


class CalcTests(TestCase):
    def test_add_numbers(self):  # all test functions must start with test
        '''Test that two numbers are added together'''
        self.assertEqual(add(3, 8), 11)  # setup and assertion are two parts of
        # test, same line in this case

    def test_subtract_numbers(self):
        '''Test that values are subtracted'''
        self.assertEqual(subtract(5, 11), 6)
