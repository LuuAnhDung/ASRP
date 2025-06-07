from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional, Length
from flask_wtf.file import FileAllowed, MultipleFileField
from ...models import Region, Status, Category

class CrimeReportForm(FlaskForm):
    case_code = StringField('Mã vụ việc', validators=[DataRequired(), Length(max=50)])
    received_date = DateField('Ngày tiếp nhận', validators=[DataRequired()], format='%Y-%m-%d')
    officer_name = StringField('Cán bộ tiếp nhận', validators=[DataRequired(), Length(max=150)])

    title = StringField('Tiêu đề', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Nội dung', validators=[DataRequired()])

    informant_name = StringField('Tên người báo cáo', validators=[Optional(), Length(max=150)])
    informant_address = StringField('Địa chỉ người báo cáo', validators=[Optional(), Length(max=255)])
    informant_phone = StringField('Số điện thoại người báo cáo', validators=[Optional(), Length(max=20)])

    status = SelectField(
        'Tình trạng xử lý',
        choices=[
            ('đã tiếp nhận', 'Đã tiếp nhận'),
            ('đang thực hiện', 'Đang thực hiện'),
            ('đã hoàn thành', 'Đã hoàn thành')
        ],
        validators=[DataRequired()]
    )

    phone_numbers = TextAreaField('Danh sách số điện thoại liên quan', validators=[Optional()])
    bank_accounts = TextAreaField('Danh sách tài khoản ngân hàng', validators=[Optional()])
    ip_addresses = TextAreaField('Thông tin địa chỉ IP', validators=[Optional()])
    websites_or_apps = TextAreaField('Website hoặc ứng dụng liên quan', validators=[Optional()])

    attachments = MultipleFileField('Tệp đính kèm', validators=[
        FileAllowed(['jpg', 'png', 'pdf', 'docx'], 'Định dạng tệp không hợp lệ')
    ])

    submit = SubmitField('Gửi báo cáo')

# class CrimeReportForm(FlaskForm):
#     region_id = SelectField('Khu vực', coerce=int, validators=[DataRequired()])
#     specific_address = StringField('Địa chỉ cụ thể', validators=[Optional()])
#     status_id = SelectField('Trạng thái', coerce=int, validators=[DataRequired()])
#     category_id = SelectField('Danh mục', coerce=int, validators=[DataRequired()])

#     title = StringField('Tiêu đề', validators=[DataRequired()])
#     content = TextAreaField('Nội dung', validators=[DataRequired()])
#     informant_name = StringField('Tên người báo cáo', validators=[Optional()])
#     informant_address = StringField('Địa chỉ người báo cáo', validators=[Optional()])
#     informant_phone = StringField('Số điện thoại', validators=[Optional()])
#     informant_id_number = StringField('Số CMND/CCCD', validators=[Optional()])

#     attachments = MultipleFileField('Tệp đính kèm', validators=[FileAllowed(['jpg', 'png', 'pdf', 'docx'], 'Định dạng không hợp lệ')])
#     submit = SubmitField('Gửi báo cáo')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.region_id.choices = [(r.id, r.name) for r in Region.query.all()]
#         self.status_id.choices = [(s.id, s.name) for s in Status.query.all()]
#         self.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
#         self.status_id.data = 1
#         self.category_id.data = 1