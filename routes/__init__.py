def init_app(app):
    from .home import home_bp
    from .dashboard import dashboard_bp
    from .user import user_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(user_bp)
