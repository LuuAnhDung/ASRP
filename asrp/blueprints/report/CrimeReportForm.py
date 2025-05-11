from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed, MultipleFileField
from ...models import Region, Status, Category

class CrimeReportForm(FlaskForm):
    region_id = SelectField('Khu vực', coerce=int, validators=[DataRequired()])
    specific_address = StringField('Địa chỉ cụ thể', validators=[Optional()])
    status_id = SelectField('Trạng thái', coerce=int, validators=[DataRequired()])
    category_id = SelectField('Danh mục', coerce=int, validators=[DataRequired()])

    title = StringField('Tiêu đề', validators=[DataRequired()])
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    informant_name = StringField('Tên người báo cáo', validators=[Optional()])
    informant_address = StringField('Địa chỉ người báo cáo', validators=[Optional()])
    informant_phone = StringField('Số điện thoại', validators=[Optional()])
    informant_id_number = StringField('Số CMND/CCCD', validators=[Optional()])

    attachments = MultipleFileField('Tệp đính kèm', validators=[FileAllowed(['jpg', 'png', 'pdf', 'docx'], 'Định dạng không hợp lệ')])
    submit = SubmitField('Gửi báo cáo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.region_id.choices = [(r.id, r.name) for r in Region.query.all()]
        self.status_id.choices = [(s.id, s.name) for s in Status.query.all()]
        self.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
        self.status_id.data = 1
        self.category_id.data = 1