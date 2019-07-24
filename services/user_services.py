# I don't know why, but it seems that if I import db outside the function, db will be not be set up.
def login_service(username, password):
    '''
    :param username: username of what the user input
    :param password: password of what the user input
    :return: 0 for success. 1 for not match.
    '''
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


def signup_service(username, password, i_code=None):
    '''
    :param i_code: invitation code
    :param username: username of what the user input
    :param password: password of what the user input
    :return: 0 for success. 1 for bad invitation. 2 for occupied username. 3 for no public registration
    '''
    from models import db
    from models.user import User
    from models.privilege import Privilege
    from secrets import token_urlsafe
    check_username_format(username)
    check_password_format(password)
    # check i_code
    invitation = None
    if i_code is None:
        # if open public registration, uncomment the following line
        # pid = 3
        return 3
    else:
        from models.invitation import Invitation
        invitation = Invitation.query.filter_by(i_code=i_code).first()
        if invitation is None:
            return 1
        pid = invitation.privilege_id
    # check username availability
    if User.query.filter_by(username=username).first() is not None:
        return 2
    # create new user
    salt = token_urlsafe(20)
    password_encode = db.session.query(db.func.SHA1(password + salt)).first()[0]
    new_user = User(username=username, password=password_encode, salt=salt, pid=pid, nickname=username)
    if invitation is not None:
        db.session.delete(invitation)
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


def issue_invitation(uid, privilege_id):
    from models.user import User
    from models.invitation import Invitation
    from models.privilege import Privilege
    from models import db
    user = User.query.filter_by(uid=uid).first()
    if user.privilege.issue_invitation:
        from secrets import token_urlsafe
        i_code = token_urlsafe(10)
        while Invitation.query.filter_by(i_code=i_code).first() is not None:
            i_code = token_urlsafe(10)
        new_invitation = Invitation(i_code=i_code, inviter_uid=uid, privilege_id=privilege_id)
        db.session.add(new_invitation)
        db.session.commit()
        return 0, i_code
    return 1, 0


def change_nickname(uid, new_nickname):
    from models.user import User
    from models import db
    user = User.query.get(uid)
    # check nickname validity
    if new_nickname is None or len(new_nickname) == 0 or len(new_nickname) > 32:
        return 1
    # change nickname
    user.nickname = new_nickname
    db.session.commit()
    return 0


def change_introduction(uid, new_introduction):
    from models.user import User
    from models import db
    user = User.query.get(uid)
    # check nickname validity
    if new_introduction is None or len(new_introduction) == 0 or len(new_introduction) > 512:
        return 1
    # change nickname
    user.introduction = new_introduction
    db.session.commit()
    return 0


def change_password(uid, old_password, new_password):
    '''
    :param uid: user id
    :param old_password: old password of what the user input
    :param new_password: new password of what the user input
    :return: 0 for success. 1 for old password not match. 2 for new password illegal.
    '''
    from models.user import User
    from models import db
    user = User.query.get(uid)
    # check if old password is correct.
    check_code = login_service(user.username, old_password)
    if check_code != 0:
        return 1
    # check new password format
    try:
        check_password_format(new_password)
    except AssertionError as e:
        return 2
    # change password
    from secrets import token_urlsafe
    new_salt = token_urlsafe(20)
    new_password_encode = db.session.query(db.func.SHA1(new_password + new_salt)).first()[0]
    user.salt = new_salt
    user.password = new_password_encode
    db.session.commit()
    return 0


def update_user(uid):
    from models.user import User
    from models import db
    user = User.query.get(uid)
    if user is not None:
        user.last_active = db.func.now()
        db.session.commit()


def get_uid_by_username(username):
    from models.user import User
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return user.uid
    return None


def get_user_by_uid(uid):
    from models.user import User
    if uid is None:
        return None
    user = User.query.filter_by(uid=uid).first()
    if user is not None:
        return user
    return None


def get_users():
    from models.user import User
    return User.query.filter_by().order_by(User.last_active.desc())
