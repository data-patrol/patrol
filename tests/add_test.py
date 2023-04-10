from unittest import TestCase

from add import add
from sub import sub


class AddTest(TestCase):
    def test_add(self):
        assert add(1, 2) == 3

    def test_sub(self):
        assert sub(3, 2) == 1