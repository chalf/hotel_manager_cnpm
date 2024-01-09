from models import Customer, KindOfRoom, Bill, Room, Employee, StayingPerson, BookingForm, room_booking_form
from web_app_package import db, app
import hashlib
from sqlalchemy import func, extract


def get_customer():
    return Customer.query.all()


def get_kind_of_room():
    return KindOfRoom.query.all()


def get_bill():
    return Bill.query.all()


def get_room(type_room=None):
    rooms = Room.query
    if type_room:
        rooms = rooms.filter(Room.kind_of_room_id.__eq__(type_room))
    return rooms.all()


# def load_products(kw=None, cate_id=None, page=None):
#     products = Product.query
#
#     if kw:
#         products = products.filter(Product.name.contains(kw))
#
#     if cate_id:
#         products = products.filter(Product.category_id.__eq__(cate_id))
#
#     if page:
#         page = int(page)
#         page_size = app.config['PAGE_SIZE']
#         start = (page - 1) * page_size
#         return products.slice(start, start + page_size)
#
#     return products.all()

def active_state_room(rooms):
    for r in rooms:
        db.session.query(Room) \
            .filter(Room.name == r) \
            .update({Room.state: 1}, synchronize_session=False)
        db.session.commit()


def unactive_state_room(rooms):
    for r in rooms:
        db.session.query(Room) \
            .filter(Room.name.contains(r)) \
            .update({Room.state: 0}, synchronize_session=False)
        db.session.commit()


def active():
    db.session.query(Room) \
        .update({Room.state: 1}, synchronize_session=False)
    db.session.commit()


# admin
def get_user_by_id(user_id):
    return Employee.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return Employee.query.filter(Employee.username.__eq__(username.strip()),
                                 Employee.password.__eq__(password)).first()


def count_products():
    return db.session.query(KindOfRoom.id, KindOfRoom.name,
                            func.count(Room.id)).join(Room,
                                                      Room.kind_of_room_id == KindOfRoom.id, isouter=True) \
        .group_by(KindOfRoom.id).all()


def revenue_by_room_in_month(month, year):
    # Thống kê doanh thu của từng phòng trong một tháng và năm cụ thể
    revenue_by_room = db.session.query(Room.name, func.sum(Bill.total).label('room_revenue')) \
        .join(BookingForm.rooms) \
        .join(Bill, Bill.booking_form_id == BookingForm.id) \
        .filter(func.extract('month', BookingForm.checkin_date) == month) \
        .filter(func.extract('year', BookingForm.checkin_date) == year) \
        .group_by(Room.name) \
        .order_by(Room.name) \
        .all()

    return revenue_by_room


def room_usage_report(month, year):
    room_usage = db.session.query(Room.name, func.count(BookingForm.id).label('usage_count')) \
        .join(room_booking_form, Room.id == room_booking_form.c.room_id) \
        .join(BookingForm, room_booking_form.c.booking_form_id == BookingForm.id) \
        .filter(func.extract('month', BookingForm.checkin_date) == month) \
        .filter(func.extract('year', BookingForm.checkin_date) == year) \
        .group_by(Room.name) \
        .order_by(Room.name) \
        .all()

    return room_usage


def room_booking_stats_revenue_for_month_year(month, year):
    room_booking_info = db.session.query(Room.name, KindOfRoom.unit_price, func.count(BookingForm.id).label('booking_count'), func.sum(func.datediff(BookingForm.checkout_date, BookingForm.checkin_date)).label('days_booked'), KindOfRoom.name) \
        .join(room_booking_form, Room.id == room_booking_form.c.room_id) \
        .join(BookingForm, room_booking_form.c.booking_form_id == BookingForm.id) \
        .join(KindOfRoom, Room.kind_of_room_id == KindOfRoom.id) \
        .filter(func.extract('month', BookingForm.checkin_date) == month,
                func.extract('year', BookingForm.checkin_date) == year) \
        .group_by(Room.name, KindOfRoom.unit_price, KindOfRoom.name).all()

    room_stats = []
    total_revenue = 0
    for room_name, unit_price, booking_count, days_booked, kind_room in room_booking_info:
        revenue = unit_price * float(days_booked)
        total_revenue += revenue
        price = unit_price
        room_stats.append({
            'Room Name': room_name,
            'Booking Count': booking_count,
            'Unit Price': price,
            'Revenue': revenue,
            'Kind Room': kind_room
        })

    for room_stat in room_stats:
        room_stat['Percentage'] = round((room_stat['Revenue'] / total_revenue) * 100, 2)

    return {'RoomStats': room_stats, 'TotalRevenue': total_revenue}


def room_utilization_report_for_month_year(month, year):
    room_utilization_info = db.session.query(Room.name,
                                             func.sum(func.datediff(BookingForm.checkout_date, BookingForm.checkin_date)).label('total_days'),
                                             func.count(BookingForm.id).label('booking_count')) \
        .join(room_booking_form, Room.id == room_booking_form.c.room_id) \
        .join(BookingForm, room_booking_form.c.booking_form_id == BookingForm.id) \
        .filter(func.extract('month', BookingForm.checkin_date) == month,
                func.extract('year', BookingForm.checkin_date) == year) \
        .group_by(Room.name).all()

    room_stats = []
    total_days_all_rooms = 0

    for room_name, total_days, booking_count in room_utilization_info:
        total_days_all_rooms += total_days
        room_stats.append({
            'Room Name': room_name,
            'Total Days Booked': total_days,
            'Booking Count': booking_count,
        })

    for room_stat in room_stats:
        room_stat['Percentage'] = round(room_stat['Total Days Booked'] / total_days_all_rooms * 100, 2)

    return room_stats


if __name__ == '__main__':
    with app.app_context():
        # print(get_room_type_info_by_month('01', "2023"))
        result = room_utilization_report_for_month_year('01', "2023")  # Ví dụ: Tháng 1 năm 2023
        print(result)
        active()
