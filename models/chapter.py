def chapter_db(db):
    """
    :type db: flask_sqlalchemy.SQLAlchemy
    """
    class Chapter(db.Model):
        cid = db.Column(db.Integer, primary_key=True)
        chapter_name = db.Column(db.String(64))

        def __init__(self, cid, chapter_name):
            self.cid = cid
            self.chapter_name = chapter_name

        def __repr__(self):
            return '<Chapter %r>' % self.chapter_name
