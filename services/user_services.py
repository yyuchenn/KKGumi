# I don't know why, but it seems that if I import db outside the function, db will be not be set up.
def login_service(username, password):
    '''
    :param username: username of what the user input
    :param password: password of what the user input
    :return: 0 for success. 1 for not match.
    '''
    # TODO
    from models import db
    from models.user import User
    check_username_format(username)
    check_password_format(password)
    pending_user = User.query.filter_by(username=username).first()
    # check if the username exists
    if pending_user is None:
        return 1
    salt = pending_user.salt
    password_encode = db.session.query(db.func.SHA1(password + salt)).first()[0]
    if password_encode == pending_user.password:
        return 0
    return 1


def signup_service(username, password, pid = 3):
    '''
    :param username: username of what the user input
    :param password: password of what the user input
    :return: 0 for success. 1 for bad invitation. 2 for occupied username.
    '''
    from models import db
    from models.user import User
    from secrets import token_urlsafe
    check_username_format(username)
    check_password_format(password)
    if User.query.filter_by(username=username).first() is not None:
        return 2
    salt = token_urlsafe(20)
    password_encode = db.session.query(db.func.SHA1(password + salt)).first()[0]
    new_user = User(username=username, password=password_encode, salt=salt)
    db.session.add(new_user)
    db.session.commit()
    return 0


def check_username_format(username):
    assert isinstance(username, str), "username is not a string."
    assert 0 < len(username) <= 32, "username is too long."


def check_password_format(password):
    from re import match
    assert isinstance(password, str), "password is not a string."
    assert 6 <= len(password) <= 32, "password is either too long or too short."
    assert match("^[\da-zA-Z_@*.#!?\- ]+$", password) is not None, "password contains illegal characters."


def issue_invitation(uid):
    from models.user import User
    from models.invitation import Invitation
    from models import db
    user = User.query.filter_by(uid=uid).first()
    if user.privilege.issue_invitation:
        from secrets import token_urlsafe
        i_code = token_urlsafe(45)
        while Invitation.query.filter_by(i_code=i_code).first() is not None:
            i_code = token_urlsafe(45)
        new_invitation = Invitation(i_code=i_code, inviter_uid=uid)
        db.session.add(new_invitation)
        db.session.commit()
        return True, i_code
    return False, 0


def get_uid_by_username(username):
    from models.user import User
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return user.uid
    return None


def get_username_by_uid(uid):
    from models.user import User
    user = User.query.filter_by(uid=uid).first()
    if user is not None:
        return user.username
    return None
