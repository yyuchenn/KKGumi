def user_db(db):
    """
    :type db: flask_sqlalchemy.SQLAlchemy
    """
    class User(db.Model):
        uid = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(32), unique=True)
        password = db.Column(db.String(128), nullable=False)
        salt = db.Column(db.String(16), nullable=False)
        gid = db.Column(db.Integer, db.ForeignKey("group.gid"))
        introduction = db.Column(db.String(512))
        gender = db.Column(db.Boolean)
        avatar = db.Column(db.LargeBinary)

        group = db.relationship("Group", backref="users")

        def __init__(self, uid, username, password, salt, gid):
            self.uid = uid
            self.username = username
            self.password = password
            self.salt = salt
            self.gid = gid

        def __repr__(self):
            return '<User %r>' % self.username
