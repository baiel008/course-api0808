from .views import UserProfileAdmin, CategoryAdmin, CourseAdmin
from fastapi import FastAPI
from sqladmin import Admin
from course_app.db.database import engine
from ..db.models import Course


def setup_admin(store_app: FastAPI):
    admin = Admin(store_app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(CourseAdmin)
