from models import db
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from routes import bootstrap
from routes.node import main as node_blue
from routes.topic import main as topic_blue
from routes.user import main as user_blue


# for db migration
from models.user import UserCls
from models.node import NodeCls
from models.topic import TopicCls

app = Flask(__name__)
manager = Manager(app)
db_path = 'forum.sqlite'
bootstrap.init_app(app)
print list(app.iter_blueprints())


def register_routes():
    app.register_blueprint(node_blue, url_prefix='/node')
    app.register_blueprint(topic_blue, url_prefix='/topic')
    app.register_blueprint(user_blue)


def configure_app():
    app.secret_key = 'luch'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    print [i.name for i in list(app.iter_blueprints())]
    #bootstrap.init_app(app)
    register_routes()


def configure_manager():
    migrate = Migrate(app, db)
    manager.add_command('db', MigrateCommand)


def configured_app():
    configure_app()
    return app


@manager.command
def server():
    print('server run')
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)

if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()