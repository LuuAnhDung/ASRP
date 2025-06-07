from flask import Blueprint, request, redirect, url_for, render_template
from .crime_routes import crime_bp
from .incident_routes import incident_bp
from .group_routes import group_bp
from .extraction_routes import extraction_bp
from .views import views_bp

from .routes import report_bp 


# from . import report_views
from ...models import CrimeReport, IncidentReport, GroupReport, ExtractionRequest

report_bp = Blueprint('report', __name__, url_prefix='/report')

@report_bp.route('/submit_report', methods=['GET', 'POST'])
def submit_report():
    if request.method == 'POST':
        # TODO: Xử lý form báo cáo
        print("Received report:", request.form)
        return redirect(url_for('report.submit_report_success'))
    return render_template('submit_report.html')

@report_bp.route('/submit_report_success')
def submit_report_success():
    return render_template('submit_report_success.html')

report_bp.register_blueprint(crime_bp)
report_bp.register_blueprint(incident_bp)
report_bp.register_blueprint(group_bp)
report_bp.register_blueprint(extraction_bp)
report_bp.register_blueprint(views_bp)

from .routes import report_statistics, export_reports, my_reports

report_bp.add_url_rule('/my-reports', view_func=my_reports)  
report_bp.add_url_rule('/statistics', view_func=report_statistics)
report_bp.add_url_rule('/export', view_func=export_reports)