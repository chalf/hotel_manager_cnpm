import models

def get_customer():
    return Customer.query.all()

def get_kind_of_room():
    return KindOfRoom.query.all()

def get_bill():
    return Bill.query.all()

def get_service():
    return Service.query.all()

def get_room():
    return Room.query.all()

