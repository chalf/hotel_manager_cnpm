import utils
import pyotp, paypalrestsdk
from flask import render_template, request, session, jsonify, redirect
from flask_login import login_user, logout_user, login_required
from web_app_package import app, list_img, data_access_objects, login
from web_app_package.data_access_objects import get_kind_of_room, get_room, active_state_room, unactive_state_room
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Thay bằng địa chỉ SMTP của bạn
app.config['MAIL_PORT'] = 587  # Thay đổi cổng SMTP nếu cần
app.config['MAIL_USERNAME'] = '2151050194khoa@ou.edu.vn'  # Thay bằng tên đăng nhập email của bạn
app.config['MAIL_PASSWORD'] = 'khoalatao123@'  # Thay bằng mật khẩu email của bạn
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


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
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)

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
    return render_template('index.html')


@app.route('/rooms')
def rooms():
    kind = get_kind_of_room()
    flag = True
    return render_template('rooms2.html', list_img=list_img, kinds_of_room=kind, flag=flag)


@app.route('/booking')
def booking():
    type_room = request.args.get('type_room')
    rooms = get_room(type_room=type_room)
    return render_template('booking.html', rooms=rooms, capacity=2)


@app.route('/booking2')
def booking2():
    num_of_guests = request.args.get('numOfGuests')
    session["numOfGuests"] = num_of_guests
    return render_template('booking2.html', numOfGuests=num_of_guests)


@app.route('/pay')
def pay():
    session["emailPayer"] = request.args.get("emailPayer")
    amount = 500
    description = "Thanh toán tiền phòng"

    paypalrestsdk.configure({
        "mode": "sandbox",  # Chế độ sandbox hoặc live
        "client_id": "AQenbzsSwZyIYheIAFCbetVGYxFgRF-OlqDlK7EpIQDb9IkVP1dFD84uRgDau6PpGVHp1JuYQSIyLjBa",
        "client_secret": "EGiHbIMLHMQGzYuvpAbZZBf-2p-i6pfZk8eGZTGGw00VBb2WmHf9f_Tw8O3-I1WJADAPtLMlTjw5sivd"
    })

    # Tạo thanh toán PayPal
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:5000/payment-success",
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
    utils.send_mail('Thông báo: Thanh toán thành công', 'Thanh toán của bạn đã được xác nhận thành công. xin cảm ơn và hẹn gặp lại!', session.get("emailPayer"))
    return render_template("index.html")


@app.route('/payment-cancel')
def payment_fail():
    utils.send_mail('Thông báo: Thanh toán thất bại', 'Thanh toán của bạn đã được xác nhận thất. xin hãy thanh toán lại! cảm ơn', session.get("emailPayer"))
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
