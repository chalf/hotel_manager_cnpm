from sqlalchemy.orm import relationship, backref

from web_app_package import db, app
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime

class CustomerBooksRoom(db.Model):
    __tablename__ = 'customer_books_room'
    customer_id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
    room_id = Column(Integer, ForeignKey('room.id'), primary_key=True)
    booking_date = Column(DateTime)
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
    booked_rooms = relationship('Room', secondary=CustomerBooksRoom.__table__, lazy='subquery',
                                backref=backref('booking_person', lazy=True))
    bill_paid = relationship('Bill', backref='payer', lazy=True)

bill_room = db.Table('bill_room',
                     Column('bill_id', Integer, ForeignKey('bill.id'), primary_key=True),
                     Column('room_id', Integer, ForeignKey('room.id'), primary_key=True))

class Room(db.Model):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    state = Column(Boolean, nullable=False)     #True là phòng trống, False là đã đặt
    number = Column(String(15))
    customer_id = Column(Integer, ForeignKey(Customer.id))
    kind_of_room_id = Column(Integer, ForeignKey('kind_of_room.id'), nullable=False)
    bills = relationship('Bill', secondary='bill_room', lazy='subquery',
                         backref=backref('rooms', lazy=True))

class KindOfRoom(db.Model):
    __tablename__ = 'kind_of_room'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    unit_price = Column(Float)
    rooms = relationship(Room, backref='kind_of_room', lazy=True)

class Bill(db.Model):
    __tablename__ = 'bill'
    id = Column(Integer, primary_key=True)
    surcharge = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        type_room1 = KindOfRoom(name='PhongTongThong', unit_price=2000000)
        db.session.add(type_room1)

        phong1 = Room(name='A01', state=True, kind_of_room_id=1)
        db.session.add(phong1)
        db.session.commit()

