from unittest import TestCase

from add import add


class AddTest(TestCase):
    def test_add(self):
        assert add(1, 2) == 3