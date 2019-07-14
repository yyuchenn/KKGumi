def init_app(app):
    from .home import home_bp
    from .dashboard import dashboard_bp
    from .content import work_bp
    from .user import user_bp
    from .admin import admin_bp
    from .guild import guild_bp
    from flask import render_template
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(work_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(guild_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    @app.errorhandler(500)
    def internal_error(error):
        import traceback
        return render_template('500.html', traceback=traceback.format_exc())
