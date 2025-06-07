from asrp import create_app
from asrp.extensions import db
from asrp.models import User, Unit, Region, Status, Category
from werkzeug.security import generate_password_hash

PROVINCES = [
    "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ", "An Giang", "Bà Rịa – Vũng Tàu",
    "Bắc Giang", "Bắc Kạn", "Bạc Liêu", "Bắc Ninh", "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước",
    "Bình Thuận", "Cà Mau", "Cao Bằng", "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp",
    "Gia Lai", "Hà Giang", "Hà Nam", "Hà Tĩnh", "Hải Dương", "Hậu Giang", "Hòa Bình", "Hưng Yên",
    "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An",
    "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Quảng Bình", "Quảng Nam", "Quảng Ngãi",
    "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình", "Thái Nguyên", "Thanh Hóa",
    "Thừa Thiên Huế", "Tiền Giang", "Trà Vinh", "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
]

UNITS = [
    ("Công an TP Hà Nội", "Đảm bảo ANTT thủ đô"),
    ("Công an TP Hồ Chí Minh", "Đảm bảo ANTT Sài Gòn"),
    ("Công an TP Bắc Ninh", "Đảm bảo ANTT Bắc Ninh"),
    ("Công an TP Bắc Giang", "Đảm bảo ANTT Bắc Giang"),
    ("Công an TP Đà Nẵng", "Đảm bảo ANTT Đà Nẵng"),
    ("Cục Cảnh sát Hình sự", "Đơn vị nghiệp vụ toàn quốc"),
    ("Công an TP Hải Phòng", "Đảm bảo ANTT Hải Phòng"),
]

STATUSES = ["Chưa xử lý", "Đang xử lý", "Đã xử lý", "Đã đóng", "Đã tiếp nhận", "Đang thực hiện"]

CATEGORIES = [
    "Báo cáo tội phạm", 
    "Báo cáo sự việc", 
    "Báo cáo nhóm tội phạm", 
    "Yêu cầu trích xuất"
]

with create_app().app_context():
    # 1) Seed 64 tỉnh/thành
    for name in PROVINCES:
        if not Region.query.filter_by(name=name).first():
            db.session.add(Region(name=name, description=f"Khu vực {name}"))
    db.session.commit()

    # 2) Seed ~5 đơn vị công an
    for name, desc in UNITS:
        if not Unit.query.filter_by(name=name).first():
            db.session.add(Unit(name=name, description=desc))
    db.session.commit()

    # 3) Seed các trạng thái
    for status_name in STATUSES:
        if not Status.query.filter_by(name=status_name).first():
            db.session.add(Status(name=status_name))
    db.session.commit()

    # 4) Seed danh mục báo cáo
    for category_name in CATEGORIES:
        if not Category.query.filter_by(name=category_name).first():
            db.session.add(Category(name=category_name))
    db.session.commit()

    # 5) Lấy một unit mặc định để gán cho user
    default_unit = Unit.query.first()

    # 6) Seed users (2 admin, 2 user) nếu chưa tồn tại
    users_data = [
        ("admin1", "admin1@example.com", "admin123", "Admin1", "0900000001", "admin"),
        ("admin2", "admin2@example.com", "admin123", "Admin2", "0900000002", "admin"),
        ("user1",  "user1@example.com",  "user123", "User1",  "0900000003", "user"),
        ("user2",  "user2@example.com",  "user123", "User2",  "0900000004", "user"),
    ]
    for uname, email, pwd, fullname, phone, role in users_data:
        if not User.query.filter_by(email=email).first():
            u = User(
                username=uname,
                email=email,
                password=generate_password_hash(pwd),
                full_name=fullname,
                phone_number=phone,
                role=role,
                unit_id=default_unit.id
            )
            db.session.add(u)
    db.session.commit()

    print("✅ Seed dữ liệu hoàn tất: 64 khu vực, 5 đơn vị, 4 trạng thái, 4 danh mục, 2 admin và 2 user.")  
