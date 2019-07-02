def manga_db(db):
    """
    :type db: flask_sqlalchemy.SQLAlchemy
    """
    class Manga(db.Model):
        mid = db.Column(db.Integer, primary_key=True)
        manga_name = db.Column(db.String(64))

        def __init__(self, mid, manga_name):
            self.mid = mid
            self.manga_name = manga_name

        def __repr__(self):
            return '<Manga %r>' % self.manga_name
