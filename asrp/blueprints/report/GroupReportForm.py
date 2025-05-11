from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

class GroupReportForm(FlaskForm):
    platform = StringField('Nền tảng', validators=[DataRequired()])
    group_name = StringField('Tên nhóm', validators=[DataRequired()])
    group_url = StringField('URL nhóm', validators=[Optional()])
    created_at = DateField('Ngày tạo', format='%Y-%m-%d', validators=[DataRequired()])
    admin_info = TextAreaField('Thông tin quản trị viên', validators=[Optional()])
    purpose = TextAreaField('Mục đích hoạt động', validators=[Optional()])
    impact_level = SelectField('Mức độ ảnh hưởng', choices=[
        ('Thấp', 'Thấp'), ('Trung bình', 'Trung bình'), ('Trung bình', 'Cao')
    ], validators=[Optional()])
    description = TextAreaField('Mô tả chi tiết', validators=[DataRequired()])
    note = TextAreaField('Ghi chú', validators=[Optional()])
    submit = SubmitField('Gửi báo cáo nhóm')
