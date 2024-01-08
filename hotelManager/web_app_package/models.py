from sqlalchemy.orm import relationship, backref
from web_app_package import db, app
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
import enum
from flask_login import UserMixin

class KindOfCustomer(db.Model):
    __tablename__ = 'kind_of_customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    multiplier = Column(Float, default=1) #hệ số nhân

    #1-n tới Customer
    customers = relationship('Customer', backref='kind_of_customer', lazy=True)

    staying_people = relationship('StayingPerson', backref = 'kind_of_customer', lazy = True)
#
# # Bảng mới từ quan hệ n-n giữa HoaDon và Phong (không phải thực thể kết hợp)
# bill_room = db.Table('bill_room',
#                      Column('bill_id', Integer, ForeignKey('bill.id'), primary_key=True),
#                      Column('room_id', Integer, ForeignKey('room.id'), primary_key=True))

class Room(db.Model):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    state = Column(Boolean, nullable=False, default=True)  # True là phòng trống, False là đã đặt

    # Tạo quan hệ 1-n đến bảng CustomerBooksRooms
    # customer_id = relationship('CustomerBooksRooms', backref='rooms')

    # Khóa ngoại 1-n tới LoaiPhong
    kind_of_room_id = Column(Integer, ForeignKey('kind_of_room.id'), nullable=False)

    # Thiết lập quan hệ n-n tới Bill khi quan hệ này không phải là 1 thực thể kết hợp, dùng secondary
    # bills = relationship('Bill', secondary='bill_room', lazy='subquery',
    #                      backref=backref('rooms', lazy=True))

class KindOfRoom(db.Model):
    __tablename__ = 'kind_of_room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    unit_price = Column(Float, default=0)
    max_number_of_customer = Column(Integer, default=3)

    # Quan hệ 1-n, tới Phong
    rooms = relationship(Room, backref='kind_of_room', lazy=True)

class Bill(db.Model):
    __tablename__ = 'bill'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total = Column(Float)
    #Tiền của 1 phòng = đơn giá phòng x (1 + phụ thu) x hệ số + tiền dịch vụ
    #Total = tổng tiền của mỗi phòng đã nhận

    # Khóa ngoại id khách hàng đã thanh toán (1-n)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

    #1-n tới Ty Le Phu Thu
    surcharge_id = Column(Integer, ForeignKey('surcharge_rate.id'), nullable=False)

    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)

    #quan hệ 1-1 với PhieuDatPhong
    booking_form = relationship('BookingForm', backref='bill', uselist=False)

# class Service(db.Model):
#     __tablename__ = 'service'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     unit_price = Column(Float,default=0)
#
#     # 1-n đến bảng CustomerUsesServices
#     customer_id = relationship('CustomerUsesServices', backref='services')
#
#     # Thiết lập quan hệ n-n tới Bill khi quan hệ này không phải là 1 thực thể kết hợp, dùng secondary
#     bills = relationship('Bill', secondary='bill_service', lazy='subquery',
#                          backref=backref('services', lazy=True))

# n-n giữa HoaDon và DichVu mà không phải thực thể kết hợp
# bill_service = db.Table('bill_service',
#                         Column('bill_id', Integer, ForeignKey('bill.id'), primary_key=True),
#                         Column('service_id', Integer, ForeignKey('service.id'), primary_key=True))

# Bảng mới - thực thể mới của KhachHang và DichVu
# class CustomerUsesServices(db.Model):
#     __tablename__ = 'customer_uses_services'
#     customer_id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
#     service_id = Column(Integer, ForeignKey('service.id'), primary_key=True)
#     using_date = Column(DateTime, primary_key=True)

class Employee(db.Model):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    user_name = Column(String(30), nullable=False)
    password = Column(String(30), nullable=False)
    active = Column(Boolean, default=True)
    role = Column(String(20))
    bills = relationship('Bill', backref = 'paid_employee', lazy = True)

class SurchargeRate(db.Model):
    __tablename__ = 'surcharge_rate'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surcharge = Column(Float, nullable=False, default=0)    #surcharge : phụ thu
    bills = relationship('Bill', backref='surcharge', lazy=True)

class BookingForm(db.Model):
    __tablename__ = 'booking_form'
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_date = Column(DateTime, primary_key=True)
    checkin_date = Column(DateTime)
    checkout_date = Column(DateTime)
    rooms = relationship('Room', secondary='room_booking_form',
                    lazy='subquery', backref=backref('booking_forms', lazy=True))
    staying_people = relationship('StayingPerson', backref = 'booking_form', lazy = True)

    #quan hệ 1-1 với HoaDon
    bill_id = Column(Integer, ForeignKey('bill.id'), unique=True, nullable=False)

    #quan he 1-n với NguoiDat
    booking_person_id = Column(Integer, ForeignKey('booking_person.id'), nullable=False)



class Customer(db.Model):   #Thực thể cha
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    cccd = Column(db.String(20), unique=True, nullable=False)
    kind_of_customer_id = Column(Integer, ForeignKey('kind_of_customer.id'), nullable=False)

    booking_people = relationship('BookingPerson', backref='customer', lazy=True)
    # addresses = relationship('Address', backref='resident', lazy=True)

class BookingPerson(db.Model):
    __tablename__ = 'booking_person'
    number = Column(db.String(20), nullable=False)
    email = Column(db.String(30), nullable=False)
    id = Column(Integer, ForeignKey('customer.id'), primary_key=True, nullable=False)
    booking_forms = relationship('BookingForm', backref = 'booking_person', lazy = True)

class StayingPerson(db.Model): #Người ở
    __tablename__ = 'staying_person'
    address = Column(String(100))
    id = Column(Integer, ForeignKey('customer.id'), primary_key=True, nullable=False)

    #quan hệ 1-n với PhieuDatPhong
    booking_form_id = Column(Integer, ForeignKey('booking_form.id'), nullable=False)

    kind_of_customer_id = Column(Integer, ForeignKey('kind_of_customer.id'), nullable=False)

#Quan hệ n-n Phiếu Đặt Phòng và Phòng
room_booking_form = db.Table('room_booking_form',
                    Column('room_id', Integer, ForeignKey('room.id'), primary_key=True),
                    Column('booking_form_id', Integer, ForeignKey('booking_form.id'), primary_key=True))

# admin
class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

        # import hashlib
        #
        # u = User(name='Admin', username='admin',
        #          password=str(hashlib.md5('20122003@'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN)
        # db.session.add(u)
        # db.session.commit()


        # type_room1 = KindOfRoom(name='Phòng Deluxe Ocean', unit_price=1400000)
        # type_room2 = KindOfRoom(name='Phòng Junior Suite Queen', unit_price=1800000)
        # type_room3 = KindOfRoom(name='Phòng Junior Suite King', unit_price=1800000)
        # type_room4 = KindOfRoom(name='Phòng Club Suite', unit_price=2400000)
        # type_room5 = KindOfRoom(name='Phòng Family Suite', unit_price=2400000)
        # db.session.add_all([type_room1, type_room2, type_room3, type_room4, type_room5])
        # db.session.commit()
        #
        p1 = Room(name='A00', state=1, kind_of_room_id=1)
        p2 = Room(name='A01', state=1, kind_of_room_id=1)
        p3 = Room(name='A02', state=1, kind_of_room_id=1)
        p4 = Room(name='A03', state=1, kind_of_room_id=1)
        p5 = Room(name='A04', state=1, kind_of_room_id=1)
        # p1 = Room(name='B00', state=1, kind_of_room_id=2)
        # p2 = Room(name='B01', state=1, kind_of_room_id=2)
        # p3 = Room(name='B02', state=1, kind_of_room_id=2)
        # p4 = Room(name='B03', state=1, kind_of_room_id=2)
        # p5 = Room(name='B04', state=1, kind_of_room_id=2)

        db.session.add_all([p1, p2, p3, p4, p5])

        db.session.commit()
