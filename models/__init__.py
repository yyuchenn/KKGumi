from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    from models import user
    from models import privilege
    from models import invitation
    from models import manga
    from models import chapter
    from models import resource
    from models import site
    db.init_app(app)
