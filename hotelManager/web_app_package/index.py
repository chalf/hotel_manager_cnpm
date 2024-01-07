from flask import render_template, request, session, jsonify, redirect

from web_app_package import app, list_img
from web_app_package.data_access_objects import get_kind_of_room, get_room, active_state_room, unactive_state_room


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
    return render_template('booking2.html')


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
    app.run(debug=True)
