from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime

from ...extensions import db
from ...models import Report, IncidentReport, Attachment, Status, Category
from .IncidentReportForm import IncidentReportForm  

incident_bp = Blueprint('incident', __name__, url_prefix='/incident')


def save_attachments(files, report_id, report_type):
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            attachment = Attachment(
                report_id=report_id,
                report_type=report_type,
                file_path=file_path,
                file_type=file.content_type,
                file_name=filename
            )
            db.session.add(attachment)


@incident_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_incident_report():
    form = IncidentReportForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            default_status = Status.query.filter_by(name="Chưa xử lý").first()
            default_category = Category.query.filter_by(name="Báo cáo sự việc").first()

            if not default_status or not default_category:
                flash("Không tìm thấy trạng thái hoặc loại báo cáo mặc định.", "error")
                return render_template('report/incident_form.html', form=form)

            report = Report(
                user_id=current_user.id,
                status_id=default_status.id, 
                category_id=default_category.id,
                created_at=datetime.utcnow()
            )
            db.session.add(report)
            db.session.flush()  # lấy report.id

            incident = IncidentReport(
                id=report.id,
                file_number=form.file_number.data,
                incident_time=form.incident_time.data,
                incident_name=form.incident_name.data,
                description=form.description.data,
                officer_name=form.officer_name.data,
                status=form.status.data,
                related_persons=form.related_persons.data,
                storage_number=form.storage_number.data,
                archived_date=form.archived_date.data
            )
            db.session.add(incident)

            save_attachments(request.files.getlist('attachments'), report.id, 'incident')
            db.session.commit()

            logging.info(f"Added incident report: {incident.incident_name}")
            flash("Báo cáo sự việc đã được thêm thành công.", "success")
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding incident report: {e}")
            flash("Có lỗi xảy ra khi thêm báo cáo sự việc.", "error")
            return render_template('report/incident_form.html', form=form)

    incidents = IncidentReport.query \
        .join(Report) \
        .filter(Report.user_id == current_user.id) \
        .order_by(Report.created_at.desc()) \
        .all()
    return render_template('report/incident_form.html', form=form, incidents=incidents)


@incident_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_incident_report(id):
    incident = IncidentReport.query.get_or_404(id)
    
    if incident.report.user_id != current_user.id:
        flash("Bạn không có quyền sửa báo cáo này.", "error")
        return redirect(url_for('report.incident.add_incident_report'))

    report = incident.report
    form = IncidentReportForm(obj=incident)

    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Cập nhật dữ liệu IncidentReport
            incident.file_number = form.file_number.data
            incident.incident_time = form.incident_time.data
            incident.incident_name = form.incident_name.data
            incident.description = form.description.data
            incident.officer_name = form.officer_name.data
            incident.status = form.status.data
            incident.related_persons = form.related_persons.data
            incident.storage_number = form.storage_number.data
            incident.archived_date = form.archived_date.data

            # Nếu bạn muốn cập nhật report (region, address) có thể thêm tại đây

            db.session.commit()
            flash("Cập nhật báo cáo sự việc thành công.", "success")
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error editing incident report {id}: {e}")
            flash("Có lỗi xảy ra khi cập nhật báo cáo sự việc.", "error")
    
    incidents = IncidentReport.query \
        .join(Report) \
        .filter(Report.user_id == current_user.id) \
        .order_by(Report.created_at.desc()) \
        .all()
    return render_template('report/incident_form.html', form=form, incidents=incidents, edit=True)


@incident_bp.route('/delete/<int:id>')
@login_required
def delete_incident_report(id):
    incident_report = IncidentReport.query.get_or_404(id)

    try:
        # Xóa tất cả đính kèm trước
        for file in incident_report.report.attachments:
            db.session.delete(file)

        # Xóa report và incident_report
        db.session.delete(incident_report.report)
        db.session.delete(incident_report)
        db.session.commit()
        flash('Xóa báo cáo thành công', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi khi xóa báo cáo: {str(e)}', 'danger')

    # Dùng đúng endpoint
    return redirect(url_for('main.index'))


@incident_bp.route('/view')
@login_required
def view_incident_reports():
    try:
        incidents = IncidentReport.query.all()
        return render_template('report/incident_list.html', incidents=incidents)
    except Exception as e:
        logging.error(f"Error loading incident reports: {e}")
        flash("Không thể tải danh sách báo cáo sự việc.", "error")
        return redirect(url_for('main.index'))
