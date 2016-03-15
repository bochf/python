from unittest import TestCase
from pydb import User


class TestUser(TestCase):
    def test_get_sessions(self):
        user = User('0000')
        user.get_sessions('room1', 'account1')
        user.dump()

    def test_dump(self):
        pass
