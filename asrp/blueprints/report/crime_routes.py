from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime

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

    if form.validate_on_submit():
        try:
            # Lấy hoặc tạo status
            status = Status.query.filter_by(name=form.status.data).first()
            if not status:
                status = Status(name=form.status.data)
                db.session.add(status)
                db.session.flush()

            # Lấy category mặc định "Báo cáo tội phạm"
            category = Category.query.filter_by(name="Báo cáo tội phạm").first()
            if not category:
                category = Category(name="Báo cáo tội phạm")
                db.session.add(category)
                db.session.flush()

            # Tạo report chung (KHÔNG có case_code)
            report = Report(
                user_id=current_user.id,
                status_id=status.id,
                category_id=category.id,
                created_at=datetime.utcnow()
            )
            db.session.add(report)
            db.session.flush()  # để lấy report.id

            # Tạo báo cáo tội phạm chi tiết
            crime = CrimeReport(
                id=report.id,
                case_code=form.case_code.data,
                received_date=form.received_date.data,
                officer_name=form.officer_name.data,
                title=form.title.data,
                content=form.content.data,
                informant_name=form.informant_name.data,
                informant_address=form.informant_address.data,
                informant_phone=form.informant_phone.data,
                status=form.status.data,
                phone_numbers=form.phone_numbers.data,
                bank_accounts=form.bank_accounts.data,
                ip_addresses=form.ip_addresses.data,
                websites_or_apps=form.websites_or_apps.data,
            )
            db.session.add(crime)

            # Lưu tệp đính kèm nếu có
            if form.attachments.data:
                save_attachments(form.attachments.data, report.id, 'crime')

            db.session.commit()
            logging.info(f"Added crime report: {crime.title}")
            flash("Báo cáo tội phạm đã được gửi thành công.", "success")
            return redirect(url_for('main.index'))

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding crime report: {e}")
            flash("Có lỗi xảy ra khi thêm báo cáo tội phạm.", "error")

    reports = CrimeReport.query \
        .join(Report) \
        .filter(Report.user_id == current_user.id) \
        .order_by(Report.created_at.desc()) \
        .all()
    return render_template('report/crime_form.html', form=form, reports=reports)

@crime_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_crime_report(id):
    report = Report.query.get_or_404(id)
    crime = CrimeReport.query.get_or_404(id)

    form = CrimeReportForm(obj=crime)

    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Cập nhật các trường chung (report)
            status = Status.query.filter_by(name=form.status.data).first()
            if not status:
                status = Status(name=form.status.data)
                db.session.add(status)
                db.session.flush()
            report.status_id = status.id

            # Cập nhật các trường riêng (crime report)
            crime.case_code = form.case_code.data
            crime.received_date = form.received_date.data
            crime.officer_name = form.officer_name.data
            crime.title = form.title.data
            crime.content = form.content.data
            crime.informant_name = form.informant_name.data
            crime.informant_address = form.informant_address.data
            crime.informant_phone = form.informant_phone.data
            crime.status = form.status.data
            crime.phone_numbers = form.phone_numbers.data
            crime.bank_accounts = form.bank_accounts.data
            crime.ip_addresses = form.ip_addresses.data
            crime.websites_or_apps = form.websites_or_apps.data

            # Lưu tệp đính kèm nếu có
            if form.attachments.data:
                save_attachments(form.attachments.data, report.id, 'crime')

            db.session.commit()
            flash("Cập nhật báo cáo tội phạm thành công.", "success")
            return redirect(url_for('main.index'))


        except Exception as e:
            db.session.rollback()
            logging.error(f"Error editing crime report {id}: {e}")
            flash("Có lỗi xảy ra khi cập nhật báo cáo.", "error")

    else:
        # Gán dữ liệu cho form (GET method)
        form.case_code.data = crime.case_code
        form.received_date.data = crime.received_date
        form.officer_name.data = crime.officer_name
        form.status.data = crime.status
        form.title.data = crime.title
        form.content.data = crime.content
        form.informant_name.data = crime.informant_name
        form.informant_address.data = crime.informant_address
        form.informant_phone.data = crime.informant_phone
        form.phone_numbers.data = crime.phone_numbers
        form.bank_accounts.data = crime.bank_accounts
        form.ip_addresses.data = crime.ip_addresses
        form.websites_or_apps.data = crime.websites_or_apps

    reports = CrimeReport.query \
        .join(Report) \
        .filter(Report.user_id == current_user.id) \
        .order_by(Report.created_at.desc()) \
        .all()
    return render_template('report/crime_form.html', form=form, edit=True)

@crime_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_crime_report(id):
    report = Report.query.get_or_404(id)
    if report.user_id != current_user.id:
        flash("Bạn không có quyền xóa báo cáo này.", "error")
        return redirect(url_for('crime.manage_crime_reports'))
    try:
        crime = CrimeReport.query.get_or_404(id)
        attachments = Attachment.query.filter_by(report_id=report.id).all()
        for att in attachments:
            try:
                if os.path.exists(att.file_path):
                    os.remove(att.file_path)
            except Exception as e:
                logging.warning(f"Không thể xóa file đính kèm: {att.file_path}. Lỗi: {e}")
            db.session.delete(att)

        db.session.delete(crime)
        db.session.delete(report)
        db.session.commit()
        flash("Đã xóa báo cáo tội phạm thành công.", "success")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting crime report {id}: {e}")
        flash("Không thể xóa báo cáo tội phạm. Vui lòng thử lại.", "error")
    return redirect(url_for('main.index'))

@crime_bp.route('/view')
@login_required
def view_crime_reports():
    try:
        reports = CrimeReport.query.join(Report).order_by(Report.created_at.desc()).all()
        return render_template('report/crime_list.html', reports=reports)
    except Exception as e:
        logging.error(f"Error loading crime reports: {e}")
        flash("Không thể tải danh sách báo cáo.", "error")
        return redirect(url_for('main.index'))
