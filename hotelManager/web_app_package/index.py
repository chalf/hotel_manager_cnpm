from flask import render_template

from web_app_package import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rooms')
def rooms():
    return render_template('rooms.html')


if __name__ == '__main__':
    app.run(debug=True)
