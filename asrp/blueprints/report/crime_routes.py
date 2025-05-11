from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
import logging

from ...extensions import db
from ...models import Report, CrimeReport, Attachment, Status, Category
from .CrimeReportForm import CrimeReportForm 

crime_bp = Blueprint('crime', __name__, url_prefix='/crime')


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


@crime_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_crime_report():
    form = CrimeReportForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            default_status = Status.query.filter_by(name="Chưa xử lý").first()
            default_category = Category.query.filter_by(name="Báo cáo tội phạm").first()

            # Nếu không tìm thấy, bạn có thể đặt giá trị mặc định
            if not default_status or not default_category:
                flash("Không tìm thấy trạng thái hoặc loại báo cáo mặc định.", "error")
                return render_template('report/crime_form.html', form=form)

            report = Report(
                user_id=current_user.id,
                region_id=form.region_id.data,
                specific_address=form.specific_address.data,
                status_id=default_status.id, 
                category_id=default_category.id 
            )
            db.session.add(report)
            db.session.flush()  # Lấy được report.id cho crime

            crime = CrimeReport(
                id=report.id,
                title=form.title.data,
                content=form.content.data,
                informant_name=form.informant_name.data,
                informant_address=form.informant_address.data,
                informant_phone=form.informant_phone.data,
                informant_id_number=form.informant_id_number.data
            )
            db.session.add(crime)

            save_attachments(request.files.getlist('attachments'), report.id, 'crime')
            db.session.commit()
            logging.info(f"Added crime report: {crime.title}")
            flash("Báo cáo tội phạm đã được gửi thành công.", "success")
            return redirect(url_for('main.index'))


        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding crime report: {e}")
            flash("Có lỗi xảy ra khi thêm báo cáo tội phạm.", "error")
            return render_template('report/crime_form.html', form=form)

    return render_template('report/crime_form.html', form=form)


@crime_bp.route('/delete/<int:id>')
@login_required
def delete_crime_report(id):
    try:
        report = CrimeReport.query.get_or_404(id)
        db.session.delete(report)
        db.session.delete(report.report)
        db.session.commit()
        logging.info(f"Deleted crime report with ID: {id}")
        flash("Đã xóa báo cáo tội phạm thành công.", "success")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting crime report with ID {id}: {e}")
        flash("Không thể xóa báo cáo tội phạm. Vui lòng thử lại.", "error")
    return redirect(url_for('report.view_all'))
