from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Optional, Length
from flask_wtf.file import FileAllowed, MultipleFileField
from ...models import Region, Status, Category



class IncidentReportForm(FlaskForm):
    file_number = StringField('Số hồ sơ', validators=[DataRequired(), Length(max=50)])
    incident_time = DateField('Thời gian xảy ra', format='%Y-%m-%d', validators=[Optional()])

    incident_name = StringField('Tên sự việc', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Mô tả sự việc', validators=[DataRequired()])

    officer_name = StringField('Cán bộ đăng ký', validators=[DataRequired(), Length(max=150)])

    status = SelectField(
        'Tình trạng xử lý',
        choices=[
            ('đã tiếp nhận', 'Đã tiếp nhận'),
            ('đang thực hiện', 'Đang thực hiện'),
            ('đã hoàn thành', 'Đã hoàn thành'),
        ],
        validators=[DataRequired()]
    )

    related_persons = TextAreaField('Người liên quan', validators=[Optional()])
    storage_number = StringField('Số lưu hồ sơ', validators=[Optional(), Length(max=100)])
    archived_date = DateField('Ngày nộp lưu', format='%Y-%m-%d', validators=[Optional()])

    attachments = MultipleFileField('Tệp đính kèm', validators=[
        FileAllowed(['jpg', 'png', 'pdf', 'docx'], 'Định dạng tệp không hợp lệ')
    ])

    submit = SubmitField('Gửi báo cáo sự việc')

# class IncidentReportForm(FlaskForm):
#     region_id = SelectField('Khu vực', coerce=int, validators=[DataRequired()])
#     specific_address = StringField('Địa chỉ cụ thể', validators=[Optional()])
#     status_id = SelectField('Trạng thái', coerce=int, validators=[DataRequired()])
#     category_id = SelectField('Danh mục', coerce=int, validators=[DataRequired()])

#     incident_name = StringField('Tên sự việc', validators=[DataRequired()])
#     description = TextAreaField('Mô tả sự việc', validators=[DataRequired()])
#     occurred_at = DateField('Thời gian xảy ra', format='%Y-%m-%d', validators=[Optional()])
#     related_people = TextAreaField('Người liên quan', validators=[Optional()])

#     attachments = MultipleFileField('Tệp đính kèm', validators=[FileAllowed(['jpg', 'png', 'pdf', 'docx'], 'Tệp không hợp lệ')])
#     submit = SubmitField('Gửi báo cáo')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.region_id.choices = [(r.id, r.name) for r in Region.query.all()]
#         self.status_id.choices = [(s.id, s.name) for s in Status.query.all()]
#         self.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
#         self.status_id.data = 1
#         self.category_id.data = 2
