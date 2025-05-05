from course_app.db.models import UserProfile, Category, Course
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]


class CourseAdmin(ModelView, model=Course):
    column_list = [Course.course_name]

