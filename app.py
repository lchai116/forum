from models import db
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from routes import bootstrap
from routes.node import main as node_blue
from routes.topic import main as topic_blue
from routes.user import main as user_blue
from routes.auth import main as auth_blue
from routes.comment import main as comment_blue
from routes.topic_api import main as topicApi_blue
from routes.backend import main as backend_blue


# import for db migration only
from models.user import UserCls
from models.node import NodeCls
from models.topic import TopicCls, CommentCls, CommentLike, TopicCollection


app = Flask(__name__)
manager = Manager(app)
db_path = 'forum.sqlite'
bootstrap.init_app(app)


def register_routes():
    app.register_blueprint(node_blue, url_prefix='/node')
    app.register_blueprint(topic_blue, url_prefix='/topic')
    app.register_blueprint(auth_blue)
    app.register_blueprint(user_blue, url_prefix='/user')
    app.register_blueprint(comment_blue, url_prefix='/comment')
    app.register_blueprint(topicApi_blue, url_prefix='/api/topic')
    app.register_blueprint(backend_blue, url_prefix='/backend')


def configure_app():
    app.secret_key = '1234'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    #bootstrap.init_app(app)
    register_routes()


def configure_manager():
    migrate = Migrate(app, db)
    manager.add_command('db', MigrateCommand)


def create_app():
    configure_app()
    return app


@manager.command
def server():
    app = create_app()
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