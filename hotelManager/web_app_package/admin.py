# from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from web_app_package import app, db, data_access_objects
# from web_app_package.models import Room
# from flask_login import logout_user, current_user
# from flask import redirect


class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name='Hotel manager', template_mode='bootstrap4', index_view=MyAdmin())
