from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
import logging

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

            # Nếu không tìm thấy, bạn có thể đặt giá trị mặc định
            if not default_status or not default_category:
                flash("Không tìm thấy trạng thái hoặc loại báo cáo mặc định.", "error")
                return render_template('report/incident_form.html', form=form)

            report = Report(
                user_id=current_user.id,
                region_id=form.region_id.data,
                specific_address=form.specific_address.data,
                status_id=default_status.id, 
                category_id=default_category.id 
            )
            db.session.add(report)
            db.session.flush()  # Lấy được report.id để gán cho incident

            incident = IncidentReport(
                id=report.id,
                incident_name=form.incident_name.data,
                description=form.description.data,
                occurred_at=form.occurred_at.data,
                related_people=form.related_people.data
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

    return render_template('report/incident_form.html', form=form)


@incident_bp.route('/delete/<int:id>')
@login_required
def delete_incident_report(id):
    try:
        incident = IncidentReport.query.get_or_404(id)
        db.session.delete(incident)
        db.session.delete(incident.report)
        db.session.commit()
        logging.info(f"Deleted incident report with ID: {id}")
        flash("Đã xóa báo cáo sự việc thành công.", "success")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting incident report with ID {id}: {e}")
        flash("Không thể xóa báo cáo sự việc. Vui lòng thử lại.", "error")
    return redirect(url_for('report.view_all'))
