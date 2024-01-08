from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from web_app_package import app, db, data_access_objects
import models
from flask_login import logout_user, current_user
from flask import redirect, request


class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=data_access_objects.count_products())


admin = Admin(app=app, name='Hotel manager', template_mode='bootstrap4', index_view=MyAdmin())


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == models.UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        month_price = request.args.get('monthPrice')
        year_price = request.args.get('yearPrice')
        month_use_room = request.args.get('monthUseRoom')
        year_use_room = request.args.get('yearUseRoom')
        if (month_use_room or year_use_room) is None:
            month_use_room = "01"
            year_use_room = "2024"
        if (month_price or year_price) is None:
            month_price = "01"
            year_price = "2024"

        return self.render('admin/stats.html', statsPrice=data_access_objects.get_total_amount(month_price, year_price),
                           monthPrice=month_price, yearPrice=year_price,
                           RoomUsageStatistics=data_access_objects.get_room_used(month_use_room, year_use_room),
                           monthRoom=month_use_room, yearRoom=year_use_room)


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()

        return redirect('/admin')


admin.add_view(AuthenticatedAdmin(models.Room, db.session))
admin.add_view(AuthenticatedAdmin(models.Service, db.session))
admin.add_view(AuthenticatedAdmin(models.KindOfRoom, db.session))
admin.add_view(StatsView(name="Statistic"))
admin.add_view(LogoutView(name='Logout'))
