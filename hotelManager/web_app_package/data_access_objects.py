import web_app_package.models

def get_customer():
    return web_app_package.Customer.query.all()

def get_kind_of_room():
    return web_app_package.KindOfRoom.query.all()
def get_room(kw):
    products = Room.query
    if kw:
        products = products.filter(Room.name.contains(kw))
    return products.all()
