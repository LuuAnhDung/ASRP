from flask import Blueprint, render_template, request, redirect, url_for, send_file
from io import BytesIO
from datetime import datetime
from asrp.models import Report 
from asrp.extensions import db

from flask_login import login_required, current_user
import pandas as pd
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
@login_required
def export_reports():
    # 1. Nhận tham số lọc
    start_date = request.form.get('start_date')
    end_date   = request.form.get('end_date')
    status     = request.form.get('status')

    # 2. Build query với joinedload
    qry = Report.query.options(
        db.joinedload(Report.user),
        db.joinedload(Report.region),
        db.joinedload(Report.status),
        db.joinedload(Report.crime_report),
        db.joinedload(Report.incident_report),
        db.joinedload(Report.group_report),
        db.joinedload(Report.extraction_request),
    )
    if start_date:
        qry = qry.filter(Report.created_at >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        qry = qry.filter(Report.created_at <= datetime.strptime(end_date, '%Y-%m-%d'))
    if status:
        qry = qry.filter(Report.status.has(name=status))

    reports = qry.order_by(Report.created_at.desc()).all()

    # 3. Tạo data riêng cho từng loại
    crime_rows, incident_rows, group_rows, extraction_rows = [], [], [], []

    for r in reports:
        common = {
            'Report ID':        r.id,
            'User':             r.user.full_name if r.user else '',
            'Status':           r.status.name if r.status else '',
            'Created At':       r.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        if r.crime_report:
            c = r.crime_report
            crime_rows.append({
                **common,
                'Case Code':      c.case_code,
                'Received Date':  c.received_date.isoformat(),
                'Officer Name':   c.officer_name,
                'Title':          c.title,
                'Content':        c.content,
                'Informant':      c.informant_name or '',
                'Phone Numbers':  c.phone_numbers or '',
                'Bank Accounts':  c.bank_accounts or '',
                'IP Addresses':   c.ip_addresses or '',
                'Websites/Apps':  c.websites_or_apps or '',
            })
        if r.incident_report:
            i = r.incident_report
            incident_rows.append({
                **common,
                'File Number':    i.file_number,
                'Incident Time':  i.incident_time.isoformat() if i.incident_time else '',
                'Incident Name':  i.incident_name,
                'Description':    i.description,
                'Officer Name':   i.officer_name,
                'Related Persons':i.related_persons or '',
                'Storage Number': i.storage_number or '',
                'Archived Date':  i.archived_date.isoformat() if i.archived_date else '',
            })
        if r.group_report:
            g = r.group_report
            group_rows.append({
                **common,
                'Platform':        g.platform,
                'Group Name':      g.group_name,
                'Group URL':       g.group_url or '',
                'GR Created At':   g.created_at.isoformat() if g.created_at else '',
                'Admin Info':      g.admin_info or '',
                'Member Count':    g.member_count,
                'Weekly Posts':    g.weekly_post_count,
                'Assigned Officer':g.assigned_officer or '',
                'Description':     g.description,
                'Note':            g.note or '',
            })
        if r.extraction_request:
            e = r.extraction_request
            extraction_rows.append({
                **common,
                'Request Number':   e.request_number,
                'Sent Date':        e.sent_date.isoformat(),
                'Result Date':      e.result_date.isoformat() if e.result_date else '',
                'Device Type':      e.device_type,
                'Device Info':      e.device_info,
                'Extraction Detail':e.extraction_detail,
                'Extraction Result':e.extraction_result or '',
                'Receiving Officer':e.receiving_officer or '',
                'Note':             e.note or '',
            })

    # 4. Xuất Excel với nhiều sheet và format
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book

        # Định nghĩa format
        header_fmt = workbook.add_format({
            'bold': True,
            'bg_color': '#DCE6F1',
            'border': 1,
            'align': 'center'
        })
        cell_fmt = workbook.add_format({'border': 1})

        def write_sheet(df_rows, sheet_name):
            if not df_rows:
                return
            df = pd.DataFrame(df_rows)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            ws = writer.sheets[sheet_name]
            # Apply header format
            for col_num, _ in enumerate(df.columns):
                ws.write(0, col_num, df.columns[col_num], header_fmt)
                # Set column widths auto (có thể điều chỉnh cố định)
                ws.set_column(col_num, col_num, 20, cell_fmt)

        write_sheet(crime_rows,      'CrimeReports')
        write_sheet(incident_rows,   'IncidentReports')
        write_sheet(group_rows,      'GroupReports')
        write_sheet(extraction_rows, 'ExtractionRequests')

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name='bao_cao.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
