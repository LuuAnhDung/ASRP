from flask import Blueprint, request, redirect, url_for, render_template
from .crime_routes import crime_bp
from .incident_routes import incident_bp
from .group_routes import group_bp
from .extraction_routes import extraction_bp
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

# @report_bp.route('/my_reports')
# def my_reports():
#     crime_reports = CrimeReport.query.all()
#     incident_reports = IncidentReport.query.all()
#     group_reports = GroupReport.query.all()
#     extraction_requests = ExtractionRequest.query.all()

#     return render_template(
#         'report/my_reports.html',
#         crime_reports=crime_reports,
#         incident_reports=incident_reports,
#         group_reports=group_reports,
#         extraction_requests=extraction_requests
#     )

report_bp.register_blueprint(crime_bp)
report_bp.register_blueprint(incident_bp)
report_bp.register_blueprint(group_bp)
report_bp.register_blueprint(extraction_bp)

from .routes import report_statistics, export_reports, my_reports

report_bp.add_url_rule('/my-reports', view_func=my_reports)  
report_bp.add_url_rule('/statistics', view_func=report_statistics)
report_bp.add_url_rule('/export', view_func=export_reports)

# from flask import Blueprint
# from .crime_routes import crime_bp
# from .incident_routes import incident_bp
# from .group_routes import group_bp
# from .extraction_routes import extraction_bp

# report_bp = Blueprint('report', __name__, url_prefix='/report')

# from . import report_views

# # Định nghĩa route trong __init__.py của report
# @report_bp.route('/submit_report', methods=['GET', 'POST'])
# def submit_report():
#     if request.method == 'POST':
#         # Xử lý báo cáo tại đây (lưu vào DB, gửi email, v.v.)
#         return redirect(url_for('report.submit_report_success'))
#     return render_template('submit_report.html')

# @report_bp.route('/submit_report_success')
# def submit_report_success():
#     return render_template('submit_report_success.html')

# @report_bp.route('/my_reports')
# def my_reports():
#     crime_reports = CrimeReport.query.all()
#     incident_reports = IncidentReport.query.all()
#     group_reports = CriminalGroupReport.query.all()
#     extraction_requests = ElectronicDataExtractionRequest.query.all()
    
#     return render_template(
#         'report/my_reports.html',
#         crime_reports=crime_reports,
#         incident_reports=incident_reports,
#         group_reports=group_reports,
#         extraction_requests=extraction_requests
#     )

# # Chú ý: bạn có thể dùng register_blueprint lồng
# report_bp.register_blueprint(crime_bp)
# report_bp.register_blueprint(incident_bp)
# report_bp.register_blueprint(group_bp)
# report_bp.register_blueprint(extraction_bp)
