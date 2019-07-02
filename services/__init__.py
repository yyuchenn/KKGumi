# Wrap all modules in this package into an object, so that it can be passed as a parameter.
class Services:
    user_services = None

    def __int__(self):
        pass


db = None
services = Services()


def init_app(my_app, my_models):
    from . import user_services
    global db, services
    db = my_models
    services.user_services = user_services
