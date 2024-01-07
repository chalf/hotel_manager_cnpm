from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from web_app_package import app, db, data_access_objects
import models
from flask_login import logout_user, current_user
from flask import redirect, request


class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


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
        kw = request.args.get('kw')

        return self.render('admin/stats.html')


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()

        return redirect('/admin')


admin.add_view(AuthenticatedAdmin(models.Room, db.session))
admin.add_view(AuthenticatedAdmin(models.Service, db.session))
admin.add_view(AuthenticatedAdmin(models.KindOfRoom, db.session))
admin.add_view(LogoutView(name='Logout'))
