from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
import logging

from ...extensions import db
from ...models import ExtractionRequest, Attachment, Category, Status, Report, Region
from .ExtractionRequestForm import ExtractionRequestForm  # Import form nếu chưa có

extraction_bp = Blueprint('extraction', __name__, url_prefix='/extraction')


def save_attachments(files, report_id, report_type):
    for file in files:
        if file and file.filename:
            try:
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)

                attachment = Attachment(
                    report_id=report_id,
                    report_type=report_type,
                    file_path=file_path,
                    file_type=file.content_type,
                    file_name=filename
                )
                db.session.add(attachment)
                logging.info(f"Saved attachment: {filename}")
            except Exception as e:
                logging.error(f"Failed to save attachment {file.filename}: {e}")

@extraction_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_extraction_request():
    form = ExtractionRequestForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Kiểm tra trùng request_number
            existing_request = ExtractionRequest.query.filter_by(request_number=form.request_number.data).first()
            if existing_request:
                flash("Số yêu cầu đã tồn tại. Vui lòng nhập số khác.", "error")
                return render_template('report/extraction_form.html', form=form)

            # Tìm trạng thái và loại báo cáo mặc định
            default_status = Status.query.filter_by(name="Chưa xử lý").first()
            default_category = Category.query.filter_by(name="Yêu cầu trích xuất").first()

            if not default_status or not default_category:
                flash("Không tìm thấy trạng thái hoặc loại báo cáo mặc định.", "error")
                return render_template('report/extraction_form.html', form=form)

            # Tạo bản ghi báo cáo gốc
            report = Report(
                user_id=current_user.id,
                # region_id=form.region_id.data,
                # specific_address=form.specific_address.data,
                status_id=default_status.id,
                category_id=default_category.id
            )
            db.session.add(report)
            db.session.flush()  # Để lấy report.id

            # Tạo bản ghi yêu cầu trích xuất
            request_obj = ExtractionRequest(
                id=report.id,
                request_number=form.request_number.data,
                requester_id=current_user.id,
                unit_id=form.unit_id.data,
                result_date=form.result_date.data,
                device_type=form.device_type.data,
                device_info=form.device_info.data,
                extraction_detail=form.extraction_detail.data,
                extraction_result=form.extraction_result.data,
                note=form.note.data
            )
            db.session.add(request_obj)

            # Lưu file đính kèm
            save_attachments(request.files.getlist('attachments'), report.id, 'extraction')

            db.session.commit()
            logging.info(f"ExtractionRequest added: {request_obj.request_number}")
            flash('Yêu cầu trích xuất đã được gửi thành công!', 'success')
            return redirect(url_for('main.index'))

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding extraction request: {e}")
            flash('Đã xảy ra lỗi khi gửi yêu cầu trích xuất.', 'error')
            return render_template('report/extraction_form.html', form=form)

    return render_template('report/extraction_form.html', form=form)

# @extraction_bp.route('/add', methods=['GET', 'POST'])
# @login_required
# def add_extraction_request():
#     form = ExtractionRequestForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         try:
#             request_obj = ExtractionRequest(
#                 request_number=form.request_number.data,
#                 requester_id=current_user.id,
#                 unit_id=form.unit_id.data,
#                 result_date=form.result_date.data,
#                 device_type=form.device_type.data,
#                 device_info=form.device_info.data,
#                 extraction_detail=form.extraction_detail.data,
#                 extraction_result=form.extraction_result.data,
#                 note=form.note.data
#             )
#             db.session.add(request_obj)
#             db.session.flush()
#             logging.info(f"ExtractionRequest created with ID: {request_obj.id}")

#             save_attachments(request.files.getlist('attachments'), request_obj.id, 'extraction')
#             db.session.commit()
#             flash('Yêu cầu trích xuất đã được gửi thành công!', 'success')
#             return redirect(url_for('main.index'))
            
#         except Exception as e:
#             db.session.rollback()
#             logging.error(f"Error adding extraction request: {e}")
#             flash('Đã xảy ra lỗi khi gửi yêu cầu trích xuất.', 'error')
#             return redirect(url_for('report.extraction.add_extraction_request'))

#     return render_template('report/extraction_form.html', form=form)


@extraction_bp.route('/delete/<int:id>')
@login_required
def delete_extraction_request(id):
    try:
        request_obj = ExtractionRequest.query.get_or_404(id)
        db.session.delete(request_obj)
        db.session.commit()
        flash('Đã xóa yêu cầu trích xuất thành công.', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting extraction request ID {id}: {e}")
        flash('Không thể xóa yêu cầu trích xuất. Vui lòng thử lại.', 'error')
    return redirect(url_for('report.view_all'))
