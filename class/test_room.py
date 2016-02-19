from unittest import TestCase
from pydb import Room


class TestRoom(TestCase):
    def test_get_accounts(self):
        room = Room("legacy1", "legacy title", "legacy description", 500);
        room.get_accounts()
        room.dump()
