def user_db(db):
    """
    :type db: flask_sqlalchemy.SQLAlchemy
    """
    class User(db.Model):
        uid = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(32), unique=True)
        password = db.Column(db.String(128), unique=True)
        salt = db.Column(db.String(16), unique=True)

        def __init__(self, uid, username, password):
            self.uid = uid
            self.username = username
            self.password = password

        def __repr__(self):
            return '<User %r>' % self.username
