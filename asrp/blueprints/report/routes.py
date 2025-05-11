from flask import Blueprint, render_template, request, redirect, url_for, send_file
from io import BytesIO
from datetime import datetime
from asrp.models import Report 
from asrp.extensions import db

from flask_login import login_required, current_user

report_bp = Blueprint('report', __name__, url_prefix='/reports')

@report_bp.route('/my-reports')
@login_required
def my_reports():
    my_reports = Report.query.filter_by(user_id=current_user.id).options(
        db.joinedload(Report.category),
        db.joinedload(Report.status),
        db.joinedload(Report.region),
        db.joinedload(Report.crime_report),
        db.joinedload(Report.incident_report),
        db.joinedload(Report.group_report)
    ).order_by(Report.created_at.desc()).all()

    return render_template('report/my_reports.html', reports=my_reports)


@report_bp.route('/statistics', methods=['GET', 'POST'])
def report_statistics():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    status = request.form.get('status')

    query = Report.query

    if start_date:
        query = query.filter(Report.created_at >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Report.created_at <= datetime.strptime(end_date, '%Y-%m-%d'))
    if status:
        query = query.filter(Report.status.has(name=status))  # Modify this line

    reports = query.order_by(Report.created_at.desc()).all()

    return render_template('report/statistics.html', reports=reports)


@report_bp.route('/export', methods=['POST'])
def export_reports():
    from io import BytesIO
    import pandas as pd

    # Nhận tham số lọc từ form
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    status_id = request.form.get('status')

    query = Report.query

    if start_date:
        query = query.filter(Report.created_at >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Report.created_at <= datetime.strptime(end_date, '%Y-%m-%d'))
    if status_id:
        query = query.filter(Report.status_id == int(status_id))  # This part already works fine

    reports = query.all()

    # Xử lý dữ liệu xuất
    data = []
    for r in reports:
        if r.crime_report:
            title = r.crime_report.title
            description = r.crime_report.description
            report_type = 'Crime Report'
        elif r.incident_report:
            title = r.incident_report.title
            description = r.incident_report.description
            report_type = 'Incident Report'
        elif r.group_report:
            title = r.group_report.title
            description = r.group_report.description
            report_type = 'Group Report'
        elif r.extraction_request:
            title = r.extraction_request.title
            description = r.extraction_request.description
            report_type = 'Extraction Request'
        else:
            title = 'N/A'
            description = 'N/A'
            report_type = 'Unknown'

        data.append({
            'Loại báo cáo': report_type,
            'Tiêu đề': title,
            'Mô tả': description,
            'Người báo cáo': r.user.full_name if r.user else 'N/A',
            'Khu vực': r.region.name if r.region else 'N/A',
            'Địa chỉ cụ thể': r.specific_address or 'N/A',
            'Trạng thái': r.status.name if r.status else 'N/A',
            'Ngày tạo': r.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'Ngày cập nhật': r.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='BaoCao')

    output.seek(0)
    return send_file(output,
                     as_attachment=True,
                     download_name='bao_cao.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
