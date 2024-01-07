from sqlalchemy.orm import relationship, backref
from web_app_package import db, app
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, text


# Bảng mới từ quan hệ n-n giữa KhachHang và Phong (trường hợp mối quan hệ này là 1 thực thể)
class CustomerBooksRooms(db.Model):
    __tablename__ = 'customer_books_rooms'
    customer_id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
    room_id = Column(Integer, ForeignKey('room.id'), primary_key=True)
    booking_date = Column(DateTime, primary_key=True)
    checkin_date = Column(DateTime)
    checkout_date = Column(DateTime)


class Customer(db.Model):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    cccd = Column(String(20), nullable=False, unique=True)
    number = Column(String(15))
    address = Column(String(100))
    customer_type = Column(String(50), nullable=False)

    # c1 = Customer(name="Lê Văn Hiếu",cccd='1234', number= 0987654321)

    # Tạo quan hệ 1-n đến bảng CustomerBooksRooms
    booked_rooms = relationship('CustomerBooksRooms', backref='customers')

    # 1-n tới HoaDon
    bill_paid = relationship('Bill', backref='payer', lazy=True)

    # 1-n tới CustomerUsesServices
    used_services = relationship('CustomerUsesServices', backref='customers')


# Bảng mới từ quan hệ n-n giữa HoaDon và Phong (không phải thực thể kết hợp)
bill_room = db.Table('bill_room',
                     Column('bill_id', Integer, ForeignKey('bill.id'), primary_key=True),
                     Column('room_id', Integer, ForeignKey('room.id'), primary_key=True))


class Room(db.Model):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False, unique=True)
    state = Column(Boolean, nullable=False)  # True là phòng trống, False là đã đặt
    # number = Column(String(15))

    # Tạo quan hệ 1-n đến bảng CustomerBooksRooms


    # Khóa ngoại 1-n tới LoaiPhong
    kind_of_room_id = Column(Integer, ForeignKey('kind_of_room.id'), nullable=False)

    # Thiết lập quan hệ n-n tới Bill khi quan hệ này không phải là 1 thực thể kết hợp, dùng secondary
    bills = relationship('Bill', secondary='bill_room', lazy='subquery',
                         backref=backref('rooms', lazy=True))


class KindOfRoom(db.Model):
    __tablename__ = 'kind_of_room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    unit_price = Column(Float, default=0)

    # Quan hệ 1-n, tới Phong
    rooms = relationship(Room, backref='kind_of_room', lazy=True)


class Bill(db.Model):
    __tablename__ = 'bill'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surcharge = Column(Float, nullable=False, default=1)

    # Khóa ngoại id khách hàng đã thanh toán (1-n)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)


class Service(db.Model):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    unit_price = Column(Float, default=0)

    # 1-n đến bảng CustomerUsesServices
    customer_id = relationship('CustomerUsesServices', backref='services')

    # Thiết lập quan hệ n-n tới Bill khi quan hệ này không phải là 1 thực thể kết hợp, dùng secondary
    bills = relationship('Bill', secondary='bill_service', lazy='subquery',
                         backref=backref('services', lazy=True))


# n-n giữa HoaDon và DichVu mà không phải thực thể kết hợp
bill_service = db.Table('bill_service',
                        Column('bill_id', Integer, ForeignKey('bill.id'), primary_key=True),
                        Column('service_id', Integer, ForeignKey('service.id'), primary_key=True))


# Bảng mới - thực thể mới của KhachHang và DichVu
class CustomerUsesServices(db.Model):
    __tablename__ = 'customer_uses_services'
    customer_id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
    service_id = Column(Integer, ForeignKey('service.id'), primary_key=True)
    using_date = Column(DateTime, primary_key=True)


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # type_room1 = KindOfRoom(name='Phòng Deluxe Ocean', unit_price=1400000)
        # type_room2 = KindOfRoom(name='Phòng Junior Suite Queen', unit_price=1800000)
        # type_room3 = KindOfRoom(name='Phòng Junior Suite King', unit_price=1800000)
        # type_room4 = KindOfRoom(name='Phòng Club Suite', unit_price=2400000)
        # type_room5 = KindOfRoom(name='Phòng Family Suite', unit_price=2400000)
        # db.session.add_all([type_room1, type_room2, type_room3, type_room4, type_room5])
        #
        # service1 = Service(name='Xe tiễn sân bay', unit_price=650000)
        # service2 = Service(name='Xe đón sân bay', unit_price=650000)
        # service3 = Service(name='Ăn tối', unit_price=450000)
        # service4 = Service(name='Ăn trưa', unit_price=250000)
        # service5 = Service(name='Honeymoon', unit_price=1000000)
        # service6 = Service(name='Bánh sinh nhật', unit_price=350000)
        # service7 = Service(name='Hoa tươi', unit_price=500000)
        # db.session.add_all([service1, service2, service3, service4, service5, service6, service7])

        # p1 = Room(name='A00', state=1, kind_of_room_id=1)
        # p2 = Room(name='A01', state=1, kind_of_room_id=1)
        # p3 = Room(name='A02', state=1, kind_of_room_id=1)
        # p4 = Room(name='A03', state=1, kind_of_room_id=1)
        # p5 = Room(name='A04', state=1, kind_of_room_id=1)
        p1 = Room(name='B00', state=1, kind_of_room_id=2)
        p2 = Room(name='B01', state=1, kind_of_room_id=2)
        p3 = Room(name='B02', state=1, kind_of_room_id=2)
        p4 = Room(name='B03', state=1, kind_of_room_id=2)
        p5 = Room(name='B04', state=1, kind_of_room_id=2)

        db.session.add_all([p1, p2, p3, p4, p5])

        db.session.commit()
