from flask import render_template

from web_app_package import app, list_img
from web_app_package.data_access_objects import get_kind_of_room


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rooms')
def rooms():
    kind = get_kind_of_room()
    flag = True
    return render_template('rooms2.html', list_img = list_img, kinds_of_room = kind, flag = flag)


if __name__ == '__main__':
    app.run(debug=True)
