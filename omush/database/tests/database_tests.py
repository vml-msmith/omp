import unittest
from omush.database import Database
from omush.database import DatabasePlayer

class MockNotifier(object):
    def subscribe(self,
                  method=None,
                  topic=None):
        pass

    def notify(self, topic, **kwargs):
        pass

class MockGame(object):
    def __init__(self):
        self.notifier = MockNotifier()

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_object(self):
        database = Database()
        player = DatabasePlayer()
        database.add_object(player)

    def test_find_player(self):
        database = Database()
        self.assertIsNone(database.find_player_by_name("Michael"))

        player = DatabasePlayer()
        player.set_name("Michael",)
        database.add_object(player)
        self.assertEquals(database.find_player_by_name("Michael"), player)
        player_two = DatabasePlayer()
        player_two.set_name("Bob")
        database.add_object(player_two)
        self.assertEquals(database.find_player_by_name("Bob"), player_two)
        self.assertEquals(database.find_player_by_name("Michael"), player)




if __name__ == '__main__':
    unittest.main()
