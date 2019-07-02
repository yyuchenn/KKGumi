from flask_sqlalchemy import SQLAlchemy

db = None


def init_app(app):
    global db
    db = SQLAlchemy(app)
    from .user import user_db
    from .ugroup import ugroup_db
    from .manga import manga_db
    from .chapter import chapter_db
    from .quest import quest_db
    user_db(db)
    ugroup_db(db)
    #manga_db(db)
    #chapter_db(db)
    #quest_db(db)
