from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ModelMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()




