import enum
import hashlib

from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
from web_app_package import db, app
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


# Quan hệ n-n Phiếu Đặt Phòng và Phòng
room_booking_form = db.Table('room_booking_form',
                             Column('room_id', Integer, ForeignKey('room.id'), primary_key=True),
                             Column('booking_form_id', Integer,
                                    ForeignKey('booking_form.id'), primary_key=True))


class KindOfCustomer(db.Model):
    __tablename__ = 'kind_of_customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    multiplier = Column(Float, default=1)  # hệ số nhân
    # 1-n tới Customer


class Room(db.Model):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    state = Column(Boolean, nullable=False, default=True)  # True là phòng trống, False là đã đặt
    # Khóa ngoại 1-n tới LoaiPhong
    kind_of_room_id = Column(Integer, ForeignKey('kind_of_room.id'), nullable=False)


class KindOfRoom(db.Model):
    __tablename__ = 'kind_of_room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    unit_price = Column(Float, default=0)
    max_number_of_customer = Column(Integer, default=3)
    # Quan hệ 1-n, tới Phong


class Bill(db.Model):
    __tablename__ = 'bill'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total = Column(Float)
    # Tiền của 1 phòng = số ngày
    # Total = tổng tiền của mỗi phòng đã nhận
    # Khóa ngoại id khách hàng đã thanh toán (1-n)
    # 1-n tới Ty Le Phu Thu
    surcharge_id = Column(Integer, ForeignKey('surcharge_rate.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    # quan hệ 1-1 với PhieuDatPhong
    booking_form_id = Column(Integer, ForeignKey('booking_form.id'), nullable=False)


class Employee(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    def __str__(self):
        return self.name


class SurchargeRate(db.Model):
    __tablename__ = 'surcharge_rate'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surcharge = Column(Float, nullable=False, default=0)  # surcharge : phụ thu


class BookingForm(db.Model):
    __tablename__ = 'booking_form'
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_date = Column(DateTime)
    checkin_date = Column(DateTime)
    checkout_date = Column(DateTime)
    # quan he 1-n với NguoiDat
    booking_person_id = Column(Integer, ForeignKey('booking_person.id'), nullable=False)
    rooms = relationship('Room', secondary='room_booking_form',
                         lazy='subquery', backref=backref('booking_forms', lazy=True))


class Customer(db.Model):  # Thực thể cha
    __tablename__ = 'customer'
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    cccd = Column(db.String(20), unique=True, nullable=False)


class BookingPerson(Customer):
    __tablename__ = 'booking_person'
    number = Column(db.String(20), nullable=False)
    email = Column(db.String(30), nullable=False)


class StayingPerson(Customer):  # Người ở
    __tablename__ = 'staying_person'
    address = Column(String(100))
    # quan hệ 1-n với PhieuDatPhong
    booking_form_id = Column(Integer, ForeignKey('booking_form.id'), nullable=False)
    kind_of_customer_id = Column(Integer, ForeignKey('kind_of_customer.id'), nullable=False)


# if __name__ == '__main__':
#     with app.app_context():
#         koc1 = KindOfCustomer(name="Foreign", multiplier=1.5)
#         koc2 = KindOfCustomer(name="In Country", multiplier=1.0)
#         db.session.add_all([koc1, koc2])
#         db.session.commit()
#         kor1 = KindOfRoom(name="Normal", unit_price=500000)
#         kor2 = KindOfRoom(name="Vip 1", unit_price=1000000)
#         kor3 = KindOfRoom(name="Vip 2", unit_price=1000000)
#         db.session.add_all([kor1, kor2, kor3])
#         db.session.commit()
#         e1 = Employee(name='Dương Trần Ngọc Hiếu', username="NhanVien",
#                       password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()))
#         e2 = Employee(name='ADMIN', username="Admin",
#                       password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.ADMIN)
#         db.session.add_all([e1,e2])
#         db.session.commit()
#         s1 = SurchargeRate(surcharge=0.25)
#         db.session.add_all([s1])
#         db.session.commit()
#
#         rr1 = Room(name="A0", kind_of_room_id=1)
#         rr2 = Room(name="A1", kind_of_room_id=1)
#         rr3 = Room(name="A2", kind_of_room_id=1)
#         rr4 = Room(name="A3", kind_of_room_id=1)
#         rr5 = Room(name="B0", kind_of_room_id=2)
#         rr6 = Room(name="B1", kind_of_room_id=2)
#         db.session.add_all([rr1, rr2, rr3, rr4, rr5, rr6])
#         db.session.commit()
#
#         bp1 = BookingPerson(name="Lê Văn Hiếu", cccd=123, number=1234, email="abc@gmail.com")
#         bp2 = BookingPerson(name="Nguyễn Minh San", cccd=2231, number=1234, email="abc@gmail.com")
#         db.session.add_all([bp1, bp2])
#         db.session.commit()
#
#         fb1 = BookingForm(booking_date='2023-01-15', checkin_date='2023-01-16', checkout_date='2023-01-17', booking_person_id=1)
#         fb2 = BookingForm(booking_date='2023-01-15', checkin_date='2023-01-16', checkout_date='2023-01-17', booking_person_id=2)
#         db.session.add_all([fb1, fb2])
#         db.session.commit()
#
#         sp1 = StayingPerson(name="Hồ Phan Tấn Khoa", cccd=2223, address="Quận 7", booking_form_id=1, kind_of_customer_id=1)
#         sp2 = StayingPerson(name="Lê Thanh Danh", cccd=333, address="Quận 12", booking_form_id=2, kind_of_customer_id=1)
#         db.session.add_all([sp1, sp2])
#         db.session.commit()
#
#         b1 = Bill(total=1000000, booking_form_id=1, surcharge_id=1, employee_id=1)
#         b2 = Bill(total=10000000, booking_form_id=2, surcharge_id=1, employee_id=1)
#         db.session.add_all([b1, b2])
#         db.session.commit()
#         # tạo quan hệ n-n Room và Phiếu đặt
#         bf1 = BookingForm.query.get(1)
#         r1 = Room.query.get(1)
#         r2 = Room.query.get(2)
#         bf1.rooms.append(r1)
#         bf1.rooms.append(r2)
#         db.session.add(bf1)
#         db.session.commit()
#
#         bf2 = BookingForm.query.get(2)
#         r3 = Room.query.get(4)
#         bf2.rooms.append(r3)
#         db.session.add(bf2)
#         db.session.commit()
