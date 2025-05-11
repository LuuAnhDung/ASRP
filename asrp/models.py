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
    extraction_requests = db.relationship('ExtractionRequest', back_populates='requester', lazy='dynamic')

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
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    informant_name = db.Column(db.String(150))
    informant_address = db.Column(db.String(255))
    informant_phone = db.Column(db.String(20))
    informant_id_number = db.Column(db.String(20))

    report = db.relationship('Report', back_populates='crime_report')


class IncidentReport(db.Model):
    __tablename__ = 'bao_cao_su_viec'

    id = db.Column(db.Integer, db.ForeignKey('bao_cao.id'), primary_key=True)
    incident_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    occurred_at = db.Column(db.DateTime)
    related_people = db.Column(db.Text)

    report = db.relationship('Report', back_populates='incident_report')


class GroupReport(db.Model):
    __tablename__ = 'bao_cao_nhom'

    id = db.Column(db.Integer, db.ForeignKey('bao_cao.id'), primary_key=True)
    platform = db.Column(db.String(100), nullable=False)
    group_name = db.Column(db.String(200), nullable=False)
    group_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    admin_info = db.Column(db.Text)
    purpose = db.Column(db.Text)
    impact_level = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text)

    report = db.relationship('Report', back_populates='group_report')


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


class ExtractionRequest(db.Model):
    __tablename__ = 'yeu_cau_trich_xuat'

    id = db.Column(db.Integer, db.ForeignKey('bao_cao.id'), primary_key=True)
    request_number = db.Column(db.String(50), unique=True, nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('don_vi.id'), nullable=False)
    result_date = db.Column(db.DateTime)
    device_type = db.Column(db.String(100), nullable=False)
    device_info = db.Column(db.Text, nullable=False)
    extraction_detail = db.Column(db.Text, nullable=False)
    extraction_result = db.Column(db.Text)
    note = db.Column(db.Text)

    report = db.relationship('Report', back_populates='extraction_request')
    requester = db.relationship('User', back_populates='extraction_requests')
    unit = db.relationship('Unit', back_populates='extraction_requests')


class LeakedInfo(db.Model):
    __tablename__ = 'thong_tin_bi_lo'

    id = db.Column(db.Integer, primary_key=True)
    contact_info = db.Column(db.String(255), nullable=False)
    info_type = db.Column(db.String(50), nullable=False)
    leaked_data = db.Column(db.Text, nullable=True)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<LeakedInfo {self.contact_info} ({self.info_type})>'
