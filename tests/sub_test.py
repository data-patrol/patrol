from unittest import TestCase

from sub import sub


class AddTest(TestCase):
    def test_sub(self):
        assert sub(3, 2) == 1