# I don't know why, but it seems that if I import db outside the function, db will be None.
def is_matched_password(username, password):
    '''
    :param username: username of what the user input
    :param password: password of what the user input
    :return: if the username matches with the password, return true, otherwise return false.
    '''
    # TODO
    if username == 'admin' and password == '123':
        return True
    return False


def signup_service(username, password):
    from . import db
    print(type(db))


def get_uid_by_username(username):
    # TODO
    return 0
