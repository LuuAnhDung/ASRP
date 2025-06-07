from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, DateTimeField, SelectField, FileField, MultipleFileField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional, URL, NumberRange
from flask_wtf.file import FileAllowed

class GroupReportForm(FlaskForm):
    platform = StringField('Nền tảng', validators=[DataRequired()])
    group_name = StringField('Tên nhóm', validators=[DataRequired()])
    group_url = StringField('URL nhóm', validators=[DataRequired()])
    created_at = DateField('Ngày tạo nhóm', format='%Y-%m-%d', validators=[Optional()])
    admin_info = TextAreaField('Thông tin quản trị viên', validators=[Optional()])

    member_count = IntegerField('Số lượng thành viên', validators=[Optional(), NumberRange(min=0)])
    weekly_post_count = IntegerField('Số bài trung bình mỗi tuần', validators=[Optional(), NumberRange(min=0)])
    status = SelectField(
        'Tình trạng xử lý',
        choices=[
            ('đã tiếp nhận', 'Đã tiếp nhận'),
            ('đang thực hiện', 'Đang thực hiện'),
            ('đã hoàn thành', 'Đã hoàn thành'),
        ],
        validators=[DataRequired()]
    )
    
    assigned_officer = StringField('Cán bộ phụ trách', validators=[Optional()])

    purpose = TextAreaField('Mục đích', validators=[Optional()])
    description = TextAreaField('Mô tả', validators=[DataRequired()])
    note = TextAreaField('Ghi chú', validators=[Optional()])

    attachments = MultipleFileField('Tệp đính kèm', validators=[Optional(), FileAllowed(['jpg', 'png', 'pdf', 'doc', 'docx', 'xls', 'xlsx'], 'Chỉ cho phép các định dạng ảnh và tài liệu')])
    
    submit = SubmitField('Gửi báo cáo')
