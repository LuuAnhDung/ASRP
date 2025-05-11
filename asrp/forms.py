from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField,
    SelectField, FloatField, DateTimeField, BooleanField, HiddenField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


# ---------- LOGIN ----------
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')


# ---------- REGISTER USER ----------
class RegisterForm(FlaskForm):
    username = StringField('Tên người dùng', validators=[DataRequired(), Length(max=64)])
    full_name = StringField('Họ và tên', validators=[DataRequired(), Length(max=150)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone_number = StringField('Số điện thoại', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Xác nhận mật khẩu', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Vai trò', choices=[('user', 'Người dùng'), ('admin', 'Quản trị viên')], validators=[DataRequired()])
    unit_id = SelectField('Đơn vị', coerce=int, validators=[DataRequired()])
    additional_info = TextAreaField('Thông tin thêm', validators=[Optional()])
    submit = SubmitField('Đăng ký')


# ---------- GENERIC REPORT ----------
class ReportForm(FlaskForm):
    area_id = SelectField('Khu vực', coerce=int, validators=[Optional()])
    detailed_address = StringField('Địa chỉ chi tiết', validators=[Optional(), Length(max=255)])
    status_id = SelectField('Trạng thái', coerce=int, validators=[DataRequired()])
    category_id = SelectField('Danh mục', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Gửi báo cáo')


# ---------- CRIME REPORT ----------
class CrimeReportForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    informant_name = StringField('Tên người cung cấp thông tin', validators=[Optional(), Length(max=150)])
    informant_address = StringField('Địa chỉ người cung cấp thông tin', validators=[Optional(), Length(max=255)])
    informant_phone = StringField('Số điện thoại người cung cấp thông tin', validators=[Optional(), Length(max=20)])
    informant_id_number = StringField('Số CMND người cung cấp thông tin', validators=[Optional(), Length(max=20)])
    submit = SubmitField('Gửi báo cáo tội phạm')


# ---------- INCIDENT REPORT ----------
class IncidentReportForm(FlaskForm):
    incident_name = StringField('Tên sự kiện', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Mô tả', validators=[DataRequired()])
    incident_time = DateTimeField('Thời gian sự kiện', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    related_persons = TextAreaField('Người liên quan', validators=[Optional()])
    submit = SubmitField('Gửi báo cáo sự kiện')


# ---------- GROUP REPORT ----------
class CrimeGroupReportForm(FlaskForm):
    platform = StringField('Nền tảng', validators=[DataRequired(), Length(max=100)])
    group_name = StringField('Tên nhóm', validators=[DataRequired(), Length(max=200)])
    group_link = StringField('Link nhóm', validators=[Optional(), Length(max=255)])
    group_created_at = DateTimeField('Ngày tạo nhóm', format='%Y-%m-%d', validators=[Optional()])
    admin_info = TextAreaField('Thông tin quản trị viên', validators=[Optional()])
    purpose = TextAreaField('Mục đích', validators=[Optional()])
    impact_level = SelectField('Mức độ tác động', coerce=int, validators=[Optional()])
    description = TextAreaField('Mô tả', validators=[DataRequired()])
    notes = TextAreaField('Ghi chú', validators=[Optional()])
    submit = SubmitField('Gửi báo cáo nhóm')


# ---------- DATA EXTRACTION REQUEST ----------
class DataExtractionForm(FlaskForm):
    request_number = StringField('Mã yêu cầu', validators=[DataRequired(), Length(max=50)])
    sender_id = SelectField('Người gửi (Người dùng)', coerce=int, validators=[DataRequired()])
    unit_id = SelectField('Đơn vị', coerce=int, validators=[DataRequired()])
    result_date = DateTimeField('Ngày kết quả', format='%Y-%m-%d', validators=[Optional()])
    device_type = StringField('Loại thiết bị', validators=[DataRequired(), Length(max=100)])
    device_info = TextAreaField('Thông tin thiết bị', validators=[DataRequired()])
    extraction_request = TextAreaField('Yêu cầu trích xuất', validators=[DataRequired()])
    extraction_result = TextAreaField('Kết quả trích xuất', validators=[Optional()])
    notes = TextAreaField('Ghi chú', validators=[Optional()])
    submit = SubmitField('Gửi yêu cầu trích xuất')


# ---------- ATTACHMENT ----------
class AttachmentForm(FlaskForm):
    report_type = SelectField('Loại báo cáo', choices=[
        ('CrimeReport', 'Báo cáo tội phạm'),
        ('IncidentReport', 'Báo cáo sự kiện'),
        ('GroupReport', 'Báo cáo nhóm'),
        ('DataExtractionRequest', 'Yêu cầu trích xuất dữ liệu'),
    ], validators=[DataRequired()])
    report_id = HiddenField('ID báo cáo')
    file_path = StringField('Đường dẫn tệp', validators=[DataRequired(), Length(max=255)])
    file_type = StringField('Loại tệp', validators=[Optional(), Length(max=20)])
    file_name = StringField('Tên tệp', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Tải lên tệp')


# ---------- CHECK INFO ----------
class CheckInfoForm(FlaskForm):
    contact_info = StringField('Email hoặc Số điện thoại', validators=[DataRequired(), Length(max=150)])
    submit = SubmitField('Kiểm tra')
