from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed, MultipleFileField
from ...models import Unit, Status, Category, ExtractionRequest, Region, Report

class ExtractionRequestForm(FlaskForm):
    request_number = StringField('Số yêu cầu', validators=[DataRequired()])
    unit_id = SelectField('Đơn vị tiếp nhận', coerce=int, validators=[DataRequired()])
    result_date = DateField('Ngày trả kết quả (nếu có)', format='%Y-%m-%d', validators=[Optional()])
    device_type = StringField('Loại thiết bị', validators=[DataRequired()])
    device_info = TextAreaField('Thông tin thiết bị', validators=[DataRequired()])
    status_id = SelectField('Trạng thái', coerce=int, validators=[DataRequired()])
    category_id = SelectField('Danh mục', coerce=int, validators=[DataRequired()])
    extraction_detail = TextAreaField('Nội dung trích xuất', validators=[DataRequired()])
    extraction_result = TextAreaField('Kết quả trích xuất', validators=[Optional()])
    note = TextAreaField('Ghi chú', validators=[Optional()])
    attachments = MultipleFileField('Tệp đính kèm', validators=[FileAllowed(['jpg', 'png', 'pdf', 'docx'], 'Chỉ cho phép file hợp lệ')])
    submit = SubmitField('Gửi yêu cầu')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unit_id.choices = [(u.id, u.name) for u in Unit.query.all()]
        self.status_id.choices = [(s.id, s.name) for s in Status.query.all()]
        self.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
        self.status_id.data = 1
        self.category_id.data = 4
