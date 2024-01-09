import phonenumbers, pycountry, paypalrestsdk
from flask_mail import Mail, Message
from web_app_package import app
from datetime import datetime
# from web_app_package.models import BookingForm, BookingPerson, StayingPerson

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
    msg = Message('Thông báo: ' + message,
                  sender='2151050194khoa@ou.edu.vn',
                  recipients=[recipients])
    msg.body = body
    mail.send(msg)
    return True


def get_total_day(dayCheckIn, dayCheckOut):
    check_in_date = datetime.strptime(dayCheckIn, '%Y-%m-%d')
    check_out_date = datetime.strptime(dayCheckOut, '%Y-%m-%d')

    delta = check_out_date - check_in_date
    num_of_days = delta.days
    return num_of_days
#
#
# def write_booking_person(fullNamePayer, cccdPayer, addressPayer, email_payer):
#     BP = BookingPerson(name=fullNamePayer, cccd=cccdPayer, number=addressPayer, email=email_payer)
#     db.session.add(BP)
#     db.session.commit()
#     db.session.flush()
#
#
# def write_booking_form(formatted_datetime, checkin_date, checkout_date, latest_booking_person):
#     BF = BookingForm(booking_date=formatted_datetime, checkin_date=checkin_date, checkout_date=checkout_date, booking_person_id=latest_booking_person)
#     db.session.add(BF)
#     db.session.commit()
#     db.session.flush()



