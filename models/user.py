from models import db


class User(db.Model):
    __tablename__ = "user"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(40), nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    pid = db.Column(db.Integer, db.ForeignKey("privilege.pid"))
    nickname = db.Column(db.String(64))
    introduction = db.Column(db.String(512))
    gender = db.Column(db.Boolean)
    avatar = db.Column(db.LargeBinary)
    join_time = db.Column(db.TIMESTAMP, default=db.func.now())
    # TODO: add last_active column

    privilege = db.relationship("Privilege", backref="users", foreign_keys="User.pid")

    '''
    def __init__(self, uid, username, password, salt, gid):
        self.uid = uid
        self.username = username
        self.password = password
        self.salt = salt
        self.gid = gid
    '''

    def __repr__(self):
        return '<User %r>' % self.username
