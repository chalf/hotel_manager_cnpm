import phonenumbers, pycountry, paypalrestsdk
from flask import redirect
from flask_mail import Mail, Message
from web_app_package import app

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Thay bằng địa chỉ SMTP của bạn
app.config['MAIL_PORT'] = 587  # Thay đổi cổng SMTP nếu cần
app.config['MAIL_USERNAME'] = '2151050194khoa@ou.edu.vn'  # Thay bằng tên đăng nhập email của bạn
app.config['MAIL_PASSWORD'] = 'khoalatao123@'  # Thay bằng mật khẩu email của bạn
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


def get_phone_codes():
    country_codes = [country.alpha_2 for country in pycountry.countries]

    countries = {}
    for region_code in phonenumbers.SUPPORTED_REGIONS:
        country_code = phonenumbers.country_code_for_region(region_code)
        country_alpha_2 = phonenumbers.region_code_for_country_code(country_code)
        if country_alpha_2 in country_codes:
            country_name = pycountry.countries.get(alpha_2=country_alpha_2).name
            countries[f'+{country_code}'] = str(country_name) + " (+" + str(country_code) + ")"

    return countries


def send_mail(message, body, recipients):
    msg = Message('Thông báo: '+message,
                  sender='2151050194khoa@ou.edu.vn',
                  recipients=[recipients])
    msg.body = body
    mail.send(msg)
    return True
