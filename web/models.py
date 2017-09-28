from pony import orm

db = orm.Database()


class User(db.Entity):
    username = orm.Required(str)
    password = orm.Required(str)
    notes = orm.Set('Note')

    @classmethod
    def all(cls):
        return cls.select()


class Note(db.Entity):
    text = orm.Required(str)
    user = orm.Required(User)
