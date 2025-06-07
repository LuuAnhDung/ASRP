from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime

from ...extensions import db
from ...models import Report, ExtractionRequest, Attachment, Status, Category, Unit, User
from .ExtractionRequestForm import ExtractionRequestForm

extraction_bp = Blueprint('extraction', __name__, url_prefix='/extraction')

def save_attachments(files, report_id, report_type):
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                os.makedirs(current_app.config['UPLOAD_FOLDER'])
            file.save(file_path)

            attachment = Attachment(
                report_id=report_id,
                report_type=report_type,
                file_path=file_path,
                file_type=file.content_type,
                file_name=filename
            )
            db.session.add(attachment)

@extraction_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_extraction_request():
    form = ExtractionRequestForm()

    # Truyền choices cho SelectField (requester, unit)
    form.unit_id.choices = [(u.id, u.name) for u in Unit.query.all()]

    if form.validate_on_submit():
        try:
            # Lấy hoặc tạo status
            status = Status.query.filter_by(name=form.status.data).first()
            if not status:
                status = Status(name=form.status.data)
                db.session.add(status)
                db.session.flush()

            # Lấy category mặc định "Yêu cầu trích xuất"
            category = Category.query.filter_by(name="Yêu cầu trích xuất").first()
            if not category:
                category = Category(name="Yêu cầu trích xuất")
                db.session.add(category)
                db.session.flush()

            # Tạo report chung
            report = Report(
                user_id=current_user.id,
                status_id=status.id,
                category_id=category.id,
                created_at=datetime.utcnow()
            )
            db.session.add(report)
            db.session.flush()

            extraction = ExtractionRequest(
                id=report.id,
                request_number=form.request_number.data,
                sent_date=form.sent_date.data,
                result_date=form.result_date.data,
                unit_id=form.unit_id.data,
                device_type=form.device_type.data,
                device_info=form.device_info.data,
                extraction_detail=form.extraction_detail.data,
                extraction_result=form.extraction_result.data,
                status=form.status.data,
                receiving_officer=form.receiving_officer.data,
                note=form.note.data
            )
            db.session.add(extraction)

            if form.attachments.data:
                save_attachments(form.attachments.data, report.id, 'extraction')

            db.session.commit()
            logging.info(f"Added extraction request: {extraction.request_number}")
            flash("Yêu cầu trích xuất đã được gửi thành công.", "success")
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding extraction request: {e}")
            flash("Có lỗi xảy ra khi thêm yêu cầu trích xuất.", "error")

    extraction_requests = ExtractionRequest.query \
        .join(Report) \
        .filter(Report.user_id == current_user.id) \
        .order_by(Report.created_at.desc()) \
        .all()
    return render_template('report/extraction_form.html', form=form, requests=extraction_requests)

@extraction_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_extraction_request(id):
    report = Report.query.get_or_404(id)
    extraction = ExtractionRequest.query.get_or_404(id)

    if report.user_id != current_user.id:
        flash("Bạn không có quyền chỉnh sửa yêu cầu này.", "error")
        return redirect(url_for('report.extraction.view_extraction_requests'))

    form = ExtractionRequestForm(obj=extraction)
    # form.requester_id.choices = [(u.id, u.username) for u in db.session.query(User).all()]
    form.unit_id.choices = [(u.id, u.name) for u in Unit.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        try:
            status = Status.query.filter_by(name=form.status.data).first()
            if not status:
                status = Status(name=form.status.data)
                db.session.add(status)
                db.session.flush()
            report.status_id = status.id

            extraction.request_number = form.request_number.data
            extraction.sent_date = form.sent_date.data
            extraction.result_date = form.result_date.data
            extraction.unit_id = form.unit_id.data
            extraction.device_type = form.device_type.data
            extraction.device_info = form.device_info.data
            extraction.extraction_detail = form.extraction_detail.data
            extraction.extraction_result = form.extraction_result.data
            extraction.status = form.status.data
            extraction.receiving_officer = form.receiving_officer.data
            extraction.note = form.note.data

            if form.attachments.data:
                save_attachments(form.attachments.data, report.id, 'extraction')

            db.session.commit()
            flash("Cập nhật yêu cầu trích xuất thành công.", "success")
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error editing extraction request {id}: {e}")
            flash("Có lỗi xảy ra khi cập nhật yêu cầu.", "error")

    else:
        # Gán lại data cho form khi GET
        form.request_number.data = extraction.request_number
        form.sent_date.data = extraction.sent_date
        form.result_date.data = extraction.result_date
        form.unit_id.data = extraction.unit_id
        form.device_type.data = extraction.device_type
        form.device_info.data = extraction.device_info
        form.extraction_detail.data = extraction.extraction_detail
        form.extraction_result.data = extraction.extraction_result
        form.status.data = extraction.status
        form.receiving_officer.data = extraction.receiving_officer
        form.note.data = extraction.note

    extraction_requests = ExtractionRequest.query \
        .join(Report) \
        .filter(Report.user_id == current_user.id) \
        .order_by(Report.created_at.desc()) \
        .all()
    return render_template('report/extraction_form.html', form=form, requests=extraction_requests)

@extraction_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_extraction_request(id):
    report = Report.query.get_or_404(id)
    if report.user_id != current_user.id:
        flash("Bạn không có quyền xóa yêu cầu này.", "error")
        return redirect(url_for('report.extraction.view_extraction_requests'))
    try:
        extraction = ExtractionRequest.query.get_or_404(id)
        attachments = Attachment.query.filter_by(report_id=report.id).all()
        for att in attachments:
            try:
                if os.path.exists(att.file_path):
                    os.remove(att.file_path)
            except Exception as e:
                logging.warning(f"Không thể xóa file đính kèm: {att.file_path}. Lỗi: {e}")
            db.session.delete(att)

        db.session.delete(extraction)
        db.session.delete(report)
        db.session.commit()
        flash("Đã xóa yêu cầu trích xuất thành công.", "success")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting extraction request {id}: {e}")
        flash("Không thể xóa yêu cầu trích xuất. Vui lòng thử lại.", "error")
    return redirect(url_for('main.index'))

@extraction_bp.route('/view')
@login_required
def view_extraction_requests():
    try:
        requests = ExtractionRequest.query.join(Report).order_by(Report.created_at.desc()).all()
        return render_template('report/extraction_list.html', requests=requests)
    except Exception as e:
        logging.error(f"Error loading extraction requests: {e}")
        flash("Không thể tải danh sách yêu cầu trích xuất.", "error")
        return redirect(url_for('main.index'))
