services = None


def init_app(app, my_services):
    global services
    services = my_services
    from .home import home_bp
    from .dashboard import dashboard_bp
    from .work import work_bp
    from .user import user_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(work_bp)
    app.register_blueprint(user_bp)
