from flask_sqlalchemy import SQLAlchemy


def init_app(app):
    from .user import user_db
    db = SQLAlchemy(app)
    user_db(db)
    return db
