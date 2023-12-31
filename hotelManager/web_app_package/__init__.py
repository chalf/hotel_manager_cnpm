from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary, cloudinary.uploader
import os

app = Flask(__name__)


app.secret_key = os.urandom(26)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/hoteldb?charset=utf8mb4" % quote('123456')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["sess_expire_on_close"] = True

db = SQLAlchemy(app)
login = LoginManager(app=app)


cloudinary.config(cloud_name='dsfdkyanf', api_key='474893993165787', api_secret='vjNSGVLgza4SMM5pvfRtnx8SFBw')
img1 = cloudinary.uploader.upload('static/img/rooms/room-1.jpg')
img2 = cloudinary.uploader.upload('static/img/rooms/room-2.jpg')
img3 = cloudinary.uploader.upload('static/img/rooms/room-3.jpg')
img4 = cloudinary.uploader.upload('static/img/rooms/room-4.jpg')
url_img1 = img1['secure_url']
url_img2 = img2['secure_url']
url_img3 = img3['secure_url']
url_img4 = img4['secure_url']
list_img = [url_img1, url_img2, url_img3, url_img4]
