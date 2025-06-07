from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime

from ...extensions import db
from ...models import Report, GroupReport, Attachment, Status, Category
from .GroupReportForm import GroupReportForm

group_bp = Blueprint('group', __name__, url_prefix='/group')

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

@group_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_group_report():
    form = GroupReportForm()

    if form.validate_on_submit():
        try:
            # Lấy hoặc tạo status
            status = Status.query.filter_by(name=form.status.data).first()
            if not status:
                status = Status(name=form.status.data)
                db.session.add(status)
                db.session.flush()

            # Lấy category mặc định "Báo cáo nhóm"
            category = Category.query.filter_by(name="Báo cáo nhóm").first()
            if not category:
                category = Category(name="Báo cáo nhóm")
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

            # Tạo GroupReport
            group = GroupReport(
                id=report.id,
                platform=form.platform.data,
                group_name=form.group_name.data,
                group_url=form.group_url.data,
                created_at=form.created_at.data,
                admin_info=form.admin_info.data,
                member_count=form.member_count.data,
                weekly_post_count=form.weekly_post_count.data,
                status=form.status.data,
                assigned_officer=form.assigned_officer.data,
                purpose=form.purpose.data,
                description=form.description.data,
                note=form.note.data
            )
            db.session.add(group)

            # Lưu tệp đính kèm nếu có
            if form.attachments.data:
                save_attachments(form.attachments.data, report.id, 'group')

            db.session.commit()
            flash("Báo cáo nhóm đã được tạo thành công.", "success")
            return redirect(url_for('main.index'))

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding group report: {e}")
            flash("Có lỗi xảy ra khi thêm báo cáo nhóm.", "error")
    reports = GroupReport.query \
        .join(Report) \
        .filter(Report.user_id == current_user.id) \
        .order_by(Report.created_at.desc()) \
        .all()

    return render_template('report/group_form.html', form=form, reports=reports)

@group_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_group_report(id):
    report = Report.query.get_or_404(id)
    group = GroupReport.query.get_or_404(id)

    form = GroupReportForm(obj=group)

    if form.validate_on_submit():
        try:
            # Cập nhật status
            status = Status.query.filter_by(name=form.status.data).first()
            if not status:
                status = Status(name=form.status.data)
                db.session.add(status)
                db.session.flush()
            report.status_id = status.id

            # Cập nhật GroupReport
            group.platform = form.platform.data
            group.group_name = form.group_name.data
            group.group_url = form.group_url.data
            group.created_at = form.created_at.data
            group.admin_info = form.admin_info.data
            group.member_count = form.member_count.data
            group.weekly_post_count = form.weekly_post_count.data
            group.status = form.status.data
            group.assigned_officer = form.assigned_officer.data
            group.purpose = form.purpose.data
            group.description = form.description.data
            group.note = form.note.data

            # Lưu tệp đính kèm nếu có
            if form.attachments.data:
                save_attachments(form.attachments.data, report.id, 'group')

            db.session.commit()
            flash("Cập nhật báo cáo nhóm thành công.", "success")
            return redirect(url_for('main.index'))

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error editing group report {id}: {e}")
            flash("Có lỗi xảy ra khi cập nhật báo cáo.", "error")
    else:
        # Pre-fill form dữ liệu nếu GET
        form.platform.data = group.platform
        form.group_name.data = group.group_name
        form.group_url.data = group.group_url
        form.created_at.data = group.created_at
        form.admin_info.data = group.admin_info
        form.member_count.data = group.member_count
        form.weekly_post_count.data = group.weekly_post_count
        form.status.data = group.status
        form.assigned_officer.data = group.assigned_officer
        form.purpose.data = group.purpose
        form.description.data = group.description
        form.note.data = group.note
    
    reports = GroupReport.query \
        .join(Report) \
        .filter(Report.user_id == current_user.id) \
        .order_by(Report.created_at.desc()) \
        .all()

    return render_template('report/group_form.html', form=form, reports=reports)

@group_bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete_group_report(id):
    try:
        group = GroupReport.query.get_or_404(id)
        report = Report.query.get_or_404(id)

        # Xoá tất cả tệp đính kèm trước
        attachments = Attachment.query.filter_by(report_id=report.id).all()
        for attachment in attachments:
            db.session.delete(attachment)

        db.session.delete(group)
        db.session.delete(report)
        db.session.commit()

        flash("Xóa báo cáo nhóm thành công.", "success")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Lỗi khi xóa group report {id}: {e}")
        flash("Có lỗi xảy ra khi xóa báo cáo nhóm.", "error")

    return redirect(url_for('main.index'))

# @group_bp.route('/delete/<int:id>', methods=['POST'])
# @login_required
# def delete_group_report(id):
#     report = Report.query.get_or_404(id)
#     if report.user_id != current_user.id:
#         flash("Bạn không có quyền xóa báo cáo này.", "error")
#         return redirect(url_for('group.view_group_reports'))
#     try:
#         group = GroupReport.query.get_or_404(id)
#         attachments = Attachment.query.filter_by(report_id=report.id).all()
#         for att in attachments:
#             try:
#                 if os.path.exists(att.file_path):
#                     os.remove(att.file_path)
#             except Exception as e:
#                 logging.warning(f"Không thể xóa file đính kèm: {att.file_path}. Lỗi: {e}")
#             db.session.delete(att)

#         db.session.delete(group)
#         db.session.delete(report)
#         db.session.commit()
#         flash("Đã xóa báo cáo nhóm thành công.", "success")
#     except Exception as e:
#         db.session.rollback()
#         logging.error(f"Error deleting group report {id}: {e}")
#         flash("Không thể xóa báo cáo nhóm. Vui lòng thử lại.", "error")
#     return redirect(url_for('group.view_group_reports'))

# @group_bp.route('/view')
# @login_required
# def view_group_reports():
#     try:
#         reports = GroupReport.query.join(Report).order_by(Report.created_at.desc()).all()
#         return render_template('report/group_list.html', reports=reports)
#     except Exception as e:
#         logging.error(f"Error loading group reports: {e}")
#         flash("Không thể tải danh sách báo cáo nhóm.", "error")
#         return redirect(url_for('main.index'))
