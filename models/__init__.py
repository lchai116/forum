from flask_sqlalchemy import SQLAlchemy
import time, random
db = SQLAlchemy()


class ModelMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        db_inst = cls.query.get(id)
        db.session.delete(db_inst)
        db.session.commit()


def unix_time():
    return int(time.time())

