from flask import Flask


def create_app():
    from .conf import CONF
    from . import services
    from . import routes
    from . import models
    my_app = Flask(__name__)
    my_app.secret_key = CONF['SECRET_KEY']
    models.init_app(my_app)
    routes.init_app(my_app)
    services.init_app(my_app)
    return my_app


if __name__ == '__main__':
    app = create_app()
    app.run()
