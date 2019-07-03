from flask import Flask
import services
import routes
import models
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


def create_app():
    my_app = Flask(__name__)
    my_app.config.from_pyfile('conf.py')
    models.init_app(my_app)
    services.init_app(my_app)
    routes.init_app(my_app)

    return my_app


app = create_app()


if __name__ == '__main__':
    from sys import argv
    if len(argv) != 1:
        '''
        To migrate/update the database:
        1) db init
        2) db migrate
        3) db upgrade
        '''
        migrate = Migrate(app, models.db)
        manager = Manager(app)
        manager.add_command('db', MigrateCommand)
        manager.run()
    else:
        app.run()
