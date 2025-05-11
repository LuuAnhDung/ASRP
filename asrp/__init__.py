from flask import Flask, render_template
from config import Config
from .extensions import db, migrate, login_manager
from .blueprints.auth import auth_bp
from .blueprints.main import main_bp
from .blueprints.report import report_bp
from .blueprints.police_officer import police_officer_bp
import logging
from logging.handlers import RotatingFileHandler

# Flask-Admin
from flask_admin import Admin
from .admin_views import AdminModelView

# Import tất cả các model
from .models import (
    User, Unit, Status, Region, Category, Report,
    CrimeReport, IncidentReport, GroupReport, Attachment, ExtractionRequest
)


def setup_logging(app):
    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=5)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    app.logger.addHandler(handler)
    app.logger.addHandler(console_handler)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.StreamHandler()])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    setup_logging(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(police_officer_bp, url_prefix='/police_officer')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    admin = Admin(app, name="ASRP Admin", template_mode='bootstrap4')

    with app.app_context():
        db.create_all()

        # Đăng ký tất cả các model với Flask-Admin
        admin.add_view(AdminModelView(User, db.session))
        admin.add_view(AdminModelView(Unit, db.session))
        admin.add_view(AdminModelView(Status, db.session))
        admin.add_view(AdminModelView(Region, db.session))
        admin.add_view(AdminModelView(Category, db.session))
        admin.add_view(AdminModelView(Report, db.session, endpoint='report_admin'))
        admin.add_view(AdminModelView(CrimeReport, db.session))
        admin.add_view(AdminModelView(IncidentReport, db.session))
        admin.add_view(AdminModelView(GroupReport, db.session))
        admin.add_view(AdminModelView(Attachment, db.session))
        admin.add_view(AdminModelView(ExtractionRequest, db.session))


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
