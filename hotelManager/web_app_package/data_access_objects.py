from models import Customer, KindOfRoom, Bill, Service, Room, User
from web_app_package import db, app
import hashlib


def get_customer():
    return Customer.query.all()


def get_kind_of_room():
    return KindOfRoom.query.all()


def get_bill():
    return Bill.query.all()


def get_service():
    return Service.query.all()


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
    return User.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


if __name__ == '__main__':
    with app.app_context():
        user = auth_user(username='admin', password='123456')
        print(user.username, user.password)
        active()
