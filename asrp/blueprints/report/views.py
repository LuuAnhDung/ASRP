from flask import Blueprint, render_template, send_file, abort
from io import BytesIO
import zipfile
import os
from ...models import Report, IncidentReport, Attachment, Status, Category

views_bp = Blueprint('views', __name__, url_prefix='/views')

# Route xem chi tiết báo cáo
@views_bp.route('/<int:id>')
def view_report(id):
    report = Report.query.get_or_404(id)
    return render_template('report/my_report.html', report=report)

@views_bp.route('/<int:id>/download')
def download_attachment(id):
    report = Report.query.get_or_404(id)

    if not report.attachments:
        abort(404)

    attachments = report.attachments  # list of Attachment objects

    # Lấy file đầu tiên để tải
    file = attachments[0]

    # Kiểm tra file có tồn tại trên ổ đĩa không trước khi gửi
    if not os.path.exists(file.file_path):
        abort(404)

    return send_file(file.file_path, as_attachment=True, download_name=file.file_name)

