class Database(object):
    def __init__(self):
        self._objects = {}
        self._nextTopObject = 0

    def add_object(self, db_object):
        if db_object.dbref() is None:
            db_object.set_dbref(self.next_dbref())

        dbref = db_object.dbref()
        if dbref in self._objects and self._objects[dbref] is not None:
            return None

        self._objects[db_object.dbref()] = db_object

        if dbref >= self.next_dbref():
            self._nextTopObject = dbref + 1

    def find_player_by_name(self, name):
        """Find a player by full name

        Return - DatabasePlayer object
        Return - None
        """
        return DatabaseMatcher.find_player_by_name(self, name)

    def get_all_objects_of_type(self, db_type):
        results = {}

        for k, v in self._objects.items():
            if v.db_type == db_type:
                results[k] = v

        return results

    def next_dbref(self):
        return self._nextTopObject

class DatabaseMatcher(object):
    @staticmethod
    def find_player_by_name(database, name):
        players = database.get_all_objects_of_type("player")
        for k, v in players.items():
            if v.name() == name:
                return v
        return None

class DatabaseObject(object):
    def __init__(self, **kwargs):
        self._db_ref = None
        self._name = "Thing"

    def set_name(self, name):
        self._name = name

    def dbref(self):
        return self._db_ref

    def set_dbref(self, dbref):
        self._db_ref = dbref

    def name(self):
        return self._name

class DatabasePlayer(DatabaseObject):
    db_type = "player"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DatabaseThing(DatabaseObject):
    db_type = "thing"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DatabaseRoom(DatabaseObject):
    db_type = "room"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DatabaseExit(DatabaseObject):
    db_type = "exit"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
