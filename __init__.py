from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


def create_app():
    import services
    import routes
    import models
    my_app = Flask(__name__)
    my_app.config.from_pyfile('conf.py')
    models.init_app(my_app)
    services.init_app(my_app, models.db)
    routes.init_app(my_app, services)
    return my_app, models.db


app, db = create_app()
print(type(db))
db.create_all()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    from sys import argv
    if len(argv) != 1:
        manager.run()
    else:
        app.run()
