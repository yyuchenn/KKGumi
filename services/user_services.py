# I don't know why, but it seems that if I import db outside the function, db will be not be set up.
def is_matched_password(username, password):
    '''
    :param username: username of what the user input
    :param password: password of what the user input
    :return: if the username matches with the password, return true, otherwise return false.
    '''
    # TODO
    check_username_format(username)
    check_password_format(password)
    if username == 'admin' and password == '123456':
        return True
    return False


def signup_service(username, password):
    from models import db, user, privilege
    check_username_format(username)
    check_password_format(password)
    g = privilege.Privilege(1)
    a = user.User(0,"admin","ac","bd",1)
    db.session.add(g)
    db.session.add(a)
    db.session.commit()


def check_username_format(username):
    assert isinstance(username, str), "username is not a string."
    assert 0 < len(username) <= 32, "username is too long."


def check_password_format(password):
    from re import match
    assert isinstance(password, str), "password is not a string."
    assert 6 <= len(password) <= 32, "password is either too long or too short."
    assert match("^[\da-zA-Z_@*.#!?\- ]+$", password) is not None, "password contains illegal characters."


def get_uid_by_username(username):
    # TODO
    return 0
