def ugroup_db(db):
    """
    :type db: flask_sqlalchemy.SQLAlchemy
    """
    class UGroup(db.Model):
        gid = db.Column(db.Integer, primary_key=True)
        group_name = db.Column(db.String(32), unique=True)

        def __init__(self, gid):
            self.gid = gid

        def __repr__(self):
            return '<Group %r>' % self.group_name