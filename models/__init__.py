from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    from models import user
    from models import privilege
    db.init_app(app)
