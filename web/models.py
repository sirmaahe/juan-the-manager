from passlib.hash import pbkdf2_sha256
from pony import orm

db = orm.Database()


class User(db.Entity):
    username = orm.Required(str)
    password = orm.Required(str)
    tg_chat = orm.Optional(int)
    notes = orm.Set('Note')

    @classmethod
    def all(cls):
        return cls.select()

    @classmethod
    def get_password(cls, password):
        return pbkdf2_sha256.encrypt(password, rounds=20000, salt_size=16)

    def compare_passwords(self, password):
        return pbkdf2_sha256.verify(password, self.password)


class Note(db.Entity):
    text = orm.Required(str)
    user = orm.Required(User)
