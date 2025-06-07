from .extensions import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Enum
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'nguoi_dung'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    role = db.Column(Enum('user', 'admin', name='user_roles'), nullable=False, default='user')
    unit_id = db.Column(db.Integer, db.ForeignKey('don_vi.id'))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    extra_info = db.Column(db.Text)

    unit = db.relationship('Unit', back_populates='users')
    reports = db.relationship('Report', back_populates='user', lazy='dynamic')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Unit(db.Model):
    __tablename__ = 'don_vi'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship('User', back_populates='unit', lazy='dynamic')
    extraction_requests = db.relationship('ExtractionRequest', back_populates='unit', lazy='dynamic')


class Status(db.Model):
    __tablename__ = 'trang_thai'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

    reports = db.relationship('Report', back_populates='status', lazy='dynamic')


class Region(db.Model):
    __tablename__ = 'khu_vuc'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    reports = db.relationship('Report', back_populates='region', lazy='dynamic')


class Category(db.Model):
    __tablename__ = 'phan_loai'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))

    reports = db.relationship('Report', back_populates='category', lazy='dynamic')


class Report(db.Model):
    __tablename__ = 'bao_cao'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id'), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('khu_vuc.id'))
    specific_address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('trang_thai.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('phan_loai.id'), nullable=False)

    user = db.relationship('User', back_populates='reports')
    region = db.relationship('Region', back_populates='reports')
    status = db.relationship('Status', back_populates='reports')
    category = db.relationship('Category', back_populates='reports')

    crime_report = db.relationship('CrimeReport', back_populates='report', uselist=False)
    incident_report = db.relationship('IncidentReport', back_populates='report', uselist=False)
    group_report = db.relationship('GroupReport', back_populates='report', uselist=False)
    extraction_request = db.relationship('ExtractionRequest', back_populates='report', uselist=False)
    attachments = db.relationship('Attachment', back_populates='report', lazy='dynamic')

    def __repr__(self):
        return f'<Report {self.id}>'

class CrimeReport(db.Model):
    __tablename__ = 'bao_cao_toi_pham'

    id = db.Column(db.Integer, db.ForeignKey('bao_cao.id'), primary_key=True)
    case_code = db.Column(db.String(50), nullable=False)  # Mã vụ việc
    received_date = db.Column(db.Date, nullable=False)  # Ngày tiếp nhận
    officer_name = db.Column(db.String(150), nullable=False)  # Cán bộ tiếp nhận

    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    informant_name = db.Column(db.String(150))
    informant_address = db.Column(db.String(255))
    informant_phone = db.Column(db.String(20))
    
    status = db.Column(db.String(50), nullable=False)  # Tình trạng xử lý

    phone_numbers = db.Column(db.Text)  # Danh sách SĐT liên quan
    bank_accounts = db.Column(db.Text)  # Danh sách tài khoản ngân hàng
    ip_addresses = db.Column(db.Text)  # Thông tin IP
    websites_or_apps = db.Column(db.Text)  # Website/Ứng dụng


    report = db.relationship('Report', back_populates='crime_report')


class IncidentReport(db.Model):
    __tablename__ = 'bao_cao_su_viec'

    id = db.Column(db.Integer, db.ForeignKey('bao_cao.id'), primary_key=True)
    file_number = db.Column(db.String(50), nullable=False)  # Số hồ sơ
    incident_time = db.Column(db.Date, nullable=True)  # Thời gian xảy ra

    incident_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    officer_name = db.Column(db.String(150), nullable=False)  # Cán bộ đăng ký
    status = db.Column(db.String(50), nullable=False)  # Tình trạng xử lý

    related_persons = db.Column(db.Text)  # Người liên quan
    storage_number = db.Column(db.String(100))  # Số lưu hồ sơ
    archived_date = db.Column(db.Date) # Ngày nộp lưu

    report = db.relationship('Report', back_populates='incident_report')


class GroupReport(db.Model):
    __tablename__ = 'bao_cao_nhom'

    id = db.Column(db.Integer, db.ForeignKey('bao_cao.id'), primary_key=True)
    
    platform = db.Column(db.String(100), nullable=False)
    group_name = db.Column(db.String(200), nullable=False)
    group_url = db.Column(db.String(255))
    created_at = db.Column(db.Date, nullable=True)
    admin_info = db.Column(db.Text)
    
    member_count = db.Column(db.Integer)  # Số lượng thành viên
    weekly_post_count = db.Column(db.Integer)  # Số bài tin trung bình mỗi tuần
    status = db.Column(db.String(50), nullable=False)  # Tình trạng xử lý
    assigned_officer = db.Column(db.String(150))  # Cán bộ phụ trách theo dõi

    purpose = db.Column(db.Text)
    description = db.Column(db.Text, nullable=False)
    
    note = db.Column(db.Text)

    report = db.relationship('Report', back_populates='group_report')

class ExtractionRequest(db.Model):
    __tablename__ = 'yeu_cau_trich_xuat'

    id = db.Column(db.Integer, db.ForeignKey('bao_cao.id'), primary_key=True)
    request_number = db.Column(db.String(50), unique=True, nullable=False)  # Số yêu cầu
    sent_date = db.Column(db.Date, nullable=False)       # Ngày gửi (chỉ ngày)
    result_date = db.Column(db.Date)                      # Ngày trả kết quả (chỉ ngày)
    
    unit_id = db.Column(db.Integer, db.ForeignKey('don_vi.id'), nullable=False)
    
    device_type = db.Column(db.String(100), nullable=False)
    device_info = db.Column(db.Text, nullable=False)
    extraction_detail = db.Column(db.Text, nullable=False)
    extraction_result = db.Column(db.Text)
    
    status = db.Column(db.String(50), nullable=False)             # Tình trạng xử lý (mới thêm)
    receiving_officer = db.Column(db.String(150))                  # Cán bộ tiếp nhận (mới thêm)

    note = db.Column(db.Text)

    report = db.relationship('Report', back_populates='extraction_request')
    unit = db.relationship('Unit', back_populates='extraction_requests')


class Attachment(db.Model):
    __tablename__ = 'tep_dinh_kem'

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('bao_cao.id'), nullable=False)
    report_type = db.Column(db.String(20))
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20))
    file_name = db.Column(db.String(200))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    report = db.relationship('Report', back_populates='attachments')