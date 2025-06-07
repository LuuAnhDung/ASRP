from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField,
    SelectField, FloatField, DateTimeField, BooleanField, HiddenField, DateField, IntegerField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


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


# ---------- Báo cáo chung ----------
class ReportForm(FlaskForm):
    area_id = SelectField('Khu vực', coerce=int, validators=[Optional()])
    detailed_address = StringField('Địa chỉ chi tiết', validators=[Optional(), Length(max=255)])
    status_id = SelectField('Trạng thái', coerce=int, validators=[DataRequired()])
    category_id = SelectField('Danh mục', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Gửi báo cáo')


# ---------- BÁO CÁO TỘI PHẠM ----------
class CrimeReportForm(FlaskForm):
    case_code = StringField('Mã vụ việc', validators=[DataRequired(), Length(max=50)])
    received_date = DateField('Ngày tiếp nhận', format='%Y-%m-%d', validators=[DataRequired()])
    officer_name = StringField('Cán bộ tiếp nhận', validators=[DataRequired(), Length(max=150)])
    title = StringField('Tiêu đề', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    
    informant_name = StringField('Công dân trình báo', validators=[Optional(), Length(max=150)])
    informant_address = StringField('Địa chỉ công dân trình báo', validators=[Optional(), Length(max=255)])
    informant_phone = StringField('Số điện thoại công dân trình báo', validators=[Optional(), Length(max=20)])
    
    status = SelectField(
        'Tình trạng xử lý',
        choices=[
            ('đã tiếp nhận', 'Đã tiếp nhận'),
            ('đang thực hiện', 'Đang thực hiện'),
            ('đã hoàn thành', 'Đã hoàn thành')
        ],
        validators=[DataRequired()]
    )

    phone_numbers = TextAreaField('Danh sách SĐT liên quan', validators=[Optional()])
    bank_accounts = TextAreaField('Danh sách tài khoản ngân hàng liên quan', validators=[Optional()])
    ip_addresses = TextAreaField('Thông tin IP liên quan', validators=[Optional()])
    websites_or_apps = TextAreaField('Website/Ứng dụng liên quan', validators=[Optional()])

    submit = SubmitField('Gửi báo cáo tội phạm')


# ---------- BÁO CÁO VỤ VIỆC ----------
class IncidentReportForm(FlaskForm):
    file_number = StringField('Số hồ sơ', validators=[DataRequired(), Length(max=50)])
    incident_time = DateTimeField('Thời gian xảy ra', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    
    incident_name = StringField('Tên vụ việc', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Nội dung vụ việc', validators=[DataRequired()])
    
    officer_name = StringField('Cán bộ đăng ký', validators=[DataRequired(), Length(max=150)])
    
    status = SelectField(
        'Tình trạng xử lý',
        choices=[
            ('đã tiếp nhận', 'Đã tiếp nhận'),
            ('đang thực hiện', 'Đang thực hiện'),
            ('đã hoàn thành', 'Đã hoàn thành')
        ],
        validators=[DataRequired()]
    )
    
    related_persons = TextAreaField('Người liên quan (mỗi người cách nhau bởi dấu phẩy)', validators=[Optional()])
    storage_number = StringField('Số lưu hồ sơ', validators=[Optional(), Length(max=100)])
    archived_date = DateField('Ngày nộp lưu', format='%Y-%m-%d', validators=[Optional()])
    
    submit = SubmitField('Gửi báo cáo sự kiện')


# ---------- BÁO CÁO NHÓM TỘI PHẠM ----------
class CrimeGroupReportForm(FlaskForm):
    platform = StringField('Nền tảng', validators=[DataRequired(), Length(max=100)])
    group_name = StringField('Tên nhóm', validators=[DataRequired(), Length(max=200)])
    group_link = StringField('Link nhóm', validators=[Optional(), Length(max=255)])
    group_created_at = DateTimeField('Ngày tạo nhóm', format='%Y-%m-%d', validators=[Optional()])
    admin_info = TextAreaField('Thông tin quản trị viên', validators=[Optional()])
    
    member_count = IntegerField('Số lượng thành viên', validators=[Optional(), NumberRange(min=0)])
    weekly_post_count = IntegerField('Số lượng bài tin trung bình mỗi tuần', validators=[Optional(), NumberRange(min=0)])
    status = SelectField(
        'Tình trạng xử lý',
        choices=[
            ('đã tiếp nhận', 'Đã tiếp nhận'),
            ('đang thực hiện', 'Đang thực hiện'),
            ('đã hoàn thành', 'Đã hoàn thành')
        ],
        validators=[DataRequired()]
    )
    assigned_officer = StringField('Cán bộ phụ trách theo dõi', validators=[Optional(), Length(max=150)])

    purpose = TextAreaField('Mục đích', validators=[Optional()])
    impact_level = SelectField('Mức độ tác động', coerce=int, validators=[Optional()])
    description = TextAreaField('Mô tả', validators=[DataRequired()])
    
    submit = SubmitField('Gửi báo cáo nhóm')


# ---------- YÊU CẦU TRÍCH XUẤT DỮ LIỆU ----------
class DataExtractionForm(FlaskForm):
    request_number = StringField('Số yêu cầu', validators=[DataRequired(), Length(max=50)])
    sent_date = DateTimeField('Ngày gửi', format='%Y-%m-%d', validators=[DataRequired()])
    result_date = DateTimeField('Ngày trả kết quả', format='%Y-%m-%d', validators=[Optional()])
    
    sender_id = SelectField('Người gửi', coerce=int, validators=[DataRequired()])
    
    unit_id = SelectField('Đơn vị tiếp nhận', coerce=int, validators=[DataRequired()])
    device_type = StringField('Loại thiết bị', validators=[DataRequired(), Length(max=100)])
    device_info = TextAreaField('Thông tin thiết bị', validators=[DataRequired()])
    
    extraction_request = TextAreaField('Yêu cầu trích xuất', validators=[DataRequired()])
    extraction_result = TextAreaField('Kết quả trích xuất', validators=[Optional()])
    status = SelectField(
        'Tình trạng xử lý',
        choices=[
            ('đã tiếp nhận', 'Đã tiếp nhận'),
            ('đang thực hiện', 'Đang thực hiện'),
            ('đã hoàn thành', 'Đã hoàn thành')
        ],
        validators=[DataRequired()]
    )
    receiving_officer = StringField('Cán bộ tiếp nhận', validators=[Optional(), Length(max=150)])
    notes = TextAreaField('Ghi chú', validators=[Optional()])
    
    submit = SubmitField('Gửi yêu cầu trích xuất')


# ---------- TỆP ĐÍNH KÈM ----------
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

