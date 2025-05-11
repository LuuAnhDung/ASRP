from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
import logging

from ...extensions import db
from ...models import GroupReport, Report
from .GroupReportForm import GroupReportForm  # Đảm bảo bạn đã tạo form này

group_bp = Blueprint('group', __name__, url_prefix='/group')


@group_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_group_report():
    form = GroupReportForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Tạo một Report trước khi tạo GroupReport
            report = Report(
                user_id=current_user.id,
                status_id=1,  # Bạn có thể thay đổi theo trạng thái mặc định
                category_id=3  # Thêm category mặc định nếu cần
            )
            db.session.add(report)
            db.session.flush()  # Để lấy được report.id

            # Tạo GroupReport liên kết với report
            group_report = GroupReport(
                id=report.id,  # Liên kết với report vừa tạo
                platform=form.platform.data,
                group_name=form.group_name.data,
                group_url=form.group_url.data,
                created_at=form.created_at.data,
                admin_info=form.admin_info.data,
                purpose=form.purpose.data,
                impact_level=form.impact_level.data,
                description=form.description.data,
                note=form.note.data
            )
            db.session.add(group_report)

            # Lưu các tệp đính kèm nếu có
            # save_attachments(request.files.getlist('attachments'), report.id, 'group')

            # Commit tất cả thay đổi vào cơ sở dữ liệu
            db.session.commit()

            logging.info(f"Group report added: {group_report.group_name}")
            flash('Báo cáo nhóm đã được thêm thành công!', 'success')
            return redirect(url_for('main.index'))  # Chuyển hướng sau khi thành công

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding group report: {e}")
            flash('Đã xảy ra lỗi khi thêm báo cáo nhóm.', 'error')
            return redirect(url_for('main.index'))

    return render_template('report/group_form.html', form=form)

# @group_bp.route('/add', methods=['GET', 'POST'])
# @login_required
# def add_group_report():
#     form = GroupReportForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         try:
#             group = GroupReport(
#                 platform=form.platform.data,
#                 group_name=form.group_name.data,
#                 group_url=form.group_url.data,
#                 created_at=form.created_at.data,
#                 admin_info=form.admin_info.data,
#                 purpose=form.purpose.data,
#                 impact_level=form.impact_level.data,
#                 description=form.description.data,
#                 note=form.note.data
#             )
#             db.session.add(group)
#             db.session.commit()
#             logging.info(f"Group report added: {group.group_name}")
#             flash('Báo cáo nhóm đã được thêm thành công!', 'success')
#             return redirect(url_for('report.view_all'))
#         except Exception as e:
#             db.session.rollback()
#             logging.error(f"Error adding group report: {e}")
#             flash('Đã xảy ra lỗi khi thêm báo cáo nhóm.', 'error')
#             return redirect(url_for('main.index'))

#     return render_template('report/group_form.html', form=form)


@group_bp.route('/delete/<int:id>')
@login_required
def delete_group_report(id):
    try:
        group = GroupReport.query.get_or_404(id)
        db.session.delete(group)
        db.session.commit()
        logging.info(f"Deleted group report with ID: {id}")
        flash('Đã xóa báo cáo nhóm thành công.', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting group report with ID {id}: {e}")
        flash('Không thể xóa báo cáo nhóm. Vui lòng thử lại.', 'error')
    return redirect(url_for('report.view_all'))
