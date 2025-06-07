from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Optional, Length
from flask_wtf.file import FileAllowed, MultipleFileField
from ...models import Unit, Status, Category, ExtractionRequest, Region, Report


class ExtractionRequestForm(FlaskForm):
    request_number = StringField('Số yêu cầu', validators=[DataRequired(), Length(max=50)])
    sent_date = DateField('Ngày gửi', format='%Y-%m-%d', validators=[DataRequired()])
    result_date = DateField('Ngày trả kết quả', format='%Y-%m-%d', validators=[Optional()])

    # requester_id và unit_id có thể là SelectField, bạn cần truyền choices từ view
    unit_id = SelectField('Đơn vị gửi yêu cầu', coerce=int, validators=[DataRequired()])

    device_type = StringField('Loại thiết bị', validators=[DataRequired(), Length(max=100)])
    device_info = TextAreaField('Thông tin thiết bị', validators=[DataRequired()])
    extraction_detail = TextAreaField('Chi tiết trích xuất', validators=[DataRequired()])
    extraction_result = TextAreaField('Kết quả trích xuất', validators=[Optional()])

    status = SelectField(
        'Tình trạng xử lý',
        choices=[
            ('đã tiếp nhận', 'Đã tiếp nhận'),
            ('đang thực hiện', 'Đang thực hiện'),
            ('đã hoàn thành', 'Đã hoàn thành'),
        ],
        validators=[DataRequired()]
    )
    receiving_officer = StringField('Cán bộ tiếp nhận', validators=[Optional(), Length(max=150)])

    note = TextAreaField('Ghi chú', validators=[Optional()])

    attachments = MultipleFileField('Tệp đính kèm', validators=[Optional(), FileAllowed(['jpg', 'png', 'pdf', 'doc', 'docx', 'xls', 'xlsx'], 'Chỉ cho phép các định dạng ảnh và tài liệu')])

    submit = SubmitField('Gửi yêu cầu')
