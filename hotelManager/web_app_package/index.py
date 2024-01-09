import utils
import pyotp, paypalrestsdk
from flask import render_template, request, session, jsonify, redirect
from flask_login import login_user, logout_user
from web_app_package import app, list_img, data_access_objects, login
from web_app_package.data_access_objects import get_kind_of_room, get_room, unactive_state_room, get_capacity, \
    get_price_of_room, add_person, add_form, write_staying_person, add_room_booking, get_id_room
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Thay bằng địa chỉ SMTP của bạn
app.config['MAIL_PORT'] = 587  # Thay đổi cổng SMTP nếu cần
app.config['MAIL_USERNAME'] = '2151050194khoa@ou.edu.vn'  # Thay bằng tên đăng nhập email của bạn
app.config['MAIL_PASSWORD'] = 'khoalatao123@'  # Thay bằng mật khẩu email của bạn
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.secret_key = "sdfsdfsdfsdafsdf"

mail = Mail(app)


# admin
@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = data_access_objects.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route("/login", methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = data_access_objects.auth_user(username=username, password=password)
        if user:
            # login_user(user=user)

            return redirect('/admin')

    return render_template('login.html')


@app.route('/logout')
def process_user_logout():
    logout_user()
    return redirect("/login")


@app.route('/statistical')
def process_statistical():
    return redirect('/admin/statsview')


@login.user_loader
def get_user(user_id):
    return data_access_objects.get_user_by_id(user_id)


# page
@app.route('/')
def index():
    try:
        session.permanent = True
        alert = session["alert"]
        session.clear()
        return render_template('index.html', alert=alert)
    except KeyError:
        alert = None
    return render_template('index.html', alert=alert)


@app.route('/rooms')
def rooms():
    kind = get_kind_of_room()
    return render_template('rooms.html', kinds_of_room=kind, list_img=list_img,
                           limit_of_img=len(list_img), limit_of_kor=len(kind))


@app.route('/booking')
def booking():
    type_room = request.args.get('type_room')
    rooms = get_room(type_room=type_room)
    capacity = get_capacity(type_room)
    session['capacity'] = capacity
    session['type_room'] = type_room
    return render_template('booking.html', rooms=rooms, capacity=capacity)


@app.route('/booking2')
def booking2():
    check_in_str = request.args.get('checkInDate')
    check_out_str = request.args.get('checkOutDate')
    total_rooms = request.args.get('numRoom')

    session['checkInDate'] = check_in_str
    session['checkOutDate'] = check_out_str
    total_days = utils.get_total_day(check_in_str, check_out_str)

    total_price = int(total_rooms) * int(total_days) * float(get_price_of_room(session['type_room']))
    session['total_price'] = int(total_price / 23000)

    num_of_guests = request.args.get('numOfGuests')
    session["numOfGuests"] = num_of_guests
    return render_template('booking2.html', numOfGuests=num_of_guests)


@app.route('/api/book_room', methods=['post'])
def book_rooms():
    data = request.json
    rooms = str(data.get("rooms")).strip().split(' ')
    if __name__ == '__main__':
        print(rooms)
    session["rooms"] = rooms


@app.route('/pay')
def pay():
    email_payer = request.args.get("emailPayer")
    fullNamePayer = request.args.get("fullNamePayer")
    cccdPayer = request.args.get("cccdPayer")
    addressPayer = request.args.get("addressPayer")
    checkin_date = session.get('checkInDate')
    checkout_date = session.get('checkOutDate')

    result = add_person(fullNamePayer, int(cccdPayer), addressPayer, email_payer)
    lf = add_form(checkout_date, checkin_date, result)
    for i in range(int(session.get("numOfGuests"))):
        fullname = request.args.get("fullName" + str(i + 1))
        CCCD = request.args.get("CCCD" + str(i + 1))
        Address = request.args.get("Address" + str(i + 1))
        write_staying_person(fullname, int(CCCD), Address, lf.id)

    rooms = session.get('rooms')

    for r in rooms:
        room = get_id_room(r)
        add_room_booking(room.id, lf.id)
    unactive_state_room(rooms)
    session["emailPayer"] = email_payer

    amount = session.get('total_price')
    description = "Thanh toán tiền phòng"
    paypalrestsdk.configure({
        "mode": "sandbox",
        "client_id": "AUuRycD9hhAEFHgVmGIyhdyLd4GnW1WQ6DRqxugFsxX87k-pK8AehnwwjXmGwhmq8z4HIGLs78Qsa2bE",
        "client_secret": "EJOz2UFyy63juDrPJ2jir8gowAxT9C35Zr5yeyHyk3XyLcT8gK8-T2C5ODERqXbDyoLXv2nfu0x3UGW7"
    })
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:5000/payment-success?pay=",
            "cancel_url": "http://localhost:5000/payment-cancel"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Item",
                    "sku": "item",
                    "price": amount,
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": amount,
                "currency": "USD"
            },
            "description": description
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                return redirect(redirect_url)
    else:
        return "Error during payment creation"


@app.route('/payment-success')
def payment_success():
    session.permanent = True
    email_payer = session.get("emailPayer")
    if email_payer:
        utils.send_mail('Notification: Payment successful',
                        'Your payment has been successfully confirmed. Thank you and see you again!', email_payer)
        session["alert"] = "1"
    return redirect("/")


@app.route('/payment-cancel')
def payment_fail():
    email_payer = request.args.get('pay')
    utils.send_mail('Notification: Payment failed',
                    'Your payment has been confirmed. Please pay again! Thanks', email_payer)
    return redirect('/pay')


# @app.route('/temp')
# def temp():
#     rooms = get_room()
#     return render_template('temp.html', rooms=rooms)
#
#
# @app.route('/temp2')
# def temp2():
#     return render_template('temp2.html')


# @app.route('/api/cart', methods=['post'])
# def add_cart():
#     cart = session.get('cart')
#     if cart is None:
#         cart = {}
#
#     data = request.json
#     id = str(data.get("id"))
#
#     if id in cart:  # san pham da co trong gio
#         cart[id]["quantity"] = cart[id]["quantity"] + 1
#     else:  # san pham chua co trong gio
#         cart[id] = {
#             "id": id,
#             "name": data.get("name"),
#             "price": data.get("price"),
#             "quantity": 1
#         }
#
#     session['cart'] = cart


@app.route('/api/book_room', methods=['post'])
def book_room():
    data = request.json
    rooms = str(data.get("rooms")).strip().split(' ')

    try:
        unactive_state_room(rooms)
    except:
        return jsonify({'status': 500, 'err_msg': 'Hệ thống đang có lỗi!'})
    else:
        return jsonify({'status': 200})


if __name__ == '__main__':
    from web_app_package import admin

    app.run(debug=True)
