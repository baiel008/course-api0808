from course_app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String, Integer, DateTime, Enum, ForeignKey,
    DECIMAL, Text, Boolean
)
from typing import Optional, List
from datetime import datetime
from enum import Enum as PyEnum


class StatusChoices(str, PyEnum):
    легкий = 'легкий'
    средний = 'средний'
    сложный = 'сложный'


class DaysChoices(str, PyEnum):
    ПН = 'ПН'
    ВТ = 'ВТ'
    СР = 'СР'
    ЧТ = 'ЧТ'
    ПТ = 'ПТ'
    СБ = 'СБ'


class RoleChoices(str, PyEnum):
    teacher = 'teacher'
    student = 'student'


class TypeChoices(str, PyEnum):
    free = 'free'
    paid = 'paid'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    profile_picture: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bio_teacher: Mapped[str] = mapped_column(Text)
    days: Mapped[DaysChoices] = mapped_column(Enum(DaysChoices), default=DaysChoices.ПН)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.легкий)
    subject: Mapped[str] = mapped_column(Text)
    experience: Mapped[int] = mapped_column(Integer)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.teacher)
    password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    user_network: Mapped[List['Network']] = relationship('Network', back_populates='user', cascade='all, delete-orphan')
    course_user_teacher: Mapped[List['Course']] = relationship('Course', back_populates='author', cascade='all, delete-orphan')
    student_assignment: Mapped[List['Assignment']] = relationship('Assignment', back_populates='students', cascade='all, delete-orphan')
    certificates_students: Mapped[List['Certificates']] = relationship('Certificates', back_populates='students', cascade='all, delete-orphan')
    course_review_user: Mapped[List['CourseReview']] = relationship('CourseReview', back_populates='user', cascade='all, delete-orphan')
    teacher_user_rating: Mapped[List['TeacherRating']] = relationship('TeacherRating', back_populates='teacher', cascade='all, delete-orphan')
    history_students: Mapped[List['History']] = relationship('History', back_populates='students', cascade='all, delete-orphan')
    cart_user: Mapped[List['Cart']] = relationship('Cart', back_populates='user', cascade='all, delete-orphan')
    user_fav: Mapped[List['Favorite']] = relationship('Favorite', back_populates='user', cascade='all, delete-orphan')
    user_token: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                            cascade='all, delete-orphan')



class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_token')
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)




class Network(Base):
    __tablename__ = 'network'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    network_name: Mapped[str] = mapped_column(String)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_network')


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String, unique=True)
    course_category: Mapped[List['Course']] = relationship('Course', back_populates='category', cascade='all, delete-orphan')


class Course(Base):
    __tablename__ = 'course'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    course_name: Mapped[str] = mapped_column(String)
    descriptions: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(Category, back_populates='course_category')
    author_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    author: Mapped[UserProfile] = relationship(UserProfile, back_populates='course_user_teacher')
    level: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.легкий)
    price: Mapped[float] = mapped_column(DECIMAL(8, 2))
    type: Mapped[TypeChoices] = mapped_column(Enum(TypeChoices), default=TypeChoices.paid)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    update_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    course_certificate: Mapped[bool] = mapped_column(Boolean, default=True)
    lesson_course: Mapped[List['Lesson']] = relationship('Lesson', back_populates='course', cascade='all, delete-orphan')
    course_exam: Mapped[List['Exam']] = relationship('Exam', back_populates='course', cascade='all, delete-orphan')
    certificates_course: Mapped[List['Certificates']] = relationship('Certificates', back_populates='course', cascade='all, delete-orphan')
    course_review_course: Mapped[List['CourseReview']] = relationship('CourseReview', back_populates='course', cascade='all, delete-orphan')
    history_course: Mapped[List['History']] = relationship('History', back_populates='course', cascade='all, delete-orphan')


class Lesson(Base):
    __tablename__ = 'lesson'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    video_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    video: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship(Course, back_populates='lesson_course')


class Assignment(Base):
    __tablename__ = 'assignment'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    due_date: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    students_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    students: Mapped[UserProfile] = relationship(UserProfile, back_populates='student_assignment')


class Exam(Base):
    __tablename__ = 'exam'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship(Course, back_populates='course_exam')
    end_time: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    exam_questions: Mapped[List['Questions']] = relationship('Questions', back_populates='exam', cascade='all, delete-orphan')


class Questions(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey('exam.id'))
    exam: Mapped[Exam] = relationship(Exam, back_populates='exam_questions')
    title: Mapped[str] = mapped_column(String)
    score: Mapped[int] = mapped_column(Integer)
    questions_option: Mapped[List['Option']] = relationship('Option', back_populates='questions', cascade='all, delete-orphan')


class Option(Base):
    __tablename__ = 'option'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    questions_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    questions: Mapped[Questions] = relationship(Questions, back_populates='questions_option')
    variant: Mapped[str] = mapped_column(String)
    option_check: Mapped[bool] = mapped_column(Boolean, default=False)


class Certificates(Base):
    __tablename__ = 'certificates'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    students_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    students: Mapped[UserProfile] = relationship(UserProfile, back_populates='certificates_students')
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship(Course, back_populates='certificates_course')
    issued_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    certificate_url: Mapped[str] = mapped_column(String)


class CourseReview(Base):
    __tablename__ = 'course_review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship(Course, back_populates='course_review_course')
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='course_review_user')
    text: Mapped[str] = mapped_column(Text)
    stars: Mapped[int] = mapped_column(Integer)


class TeacherRating(Base):
    __tablename__ = 'teacher_rating'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    teacher: Mapped[UserProfile] = relationship(UserProfile, back_populates='teacher_user_rating')
    stars: Mapped[int] = mapped_column(Integer)


class History(Base):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    students_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    students: Mapped[UserProfile] = relationship(UserProfile, back_populates='history_students')
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship(Course, back_populates='history_course')


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), unique=True)
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='cart_user')
    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'cartitem'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    cart: Mapped[Cart] = relationship(Cart, back_populates='items')
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship(Course)
    quantity: Mapped[int] = mapped_column(Integer, default=1)


class Favorite(Base):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), unique=True)
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_fav')
    fav_item: Mapped[List['FavoriteItem']] = relationship('FavoriteItem', back_populates='favorite', cascade='all, delete-orphan')


class FavoriteItem(Base):
    __tablename__ = 'favoriteitem'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    favorite_id: Mapped[int] = mapped_column(ForeignKey('favorite.id'))
    favorite: Mapped[Favorite] = relationship(Favorite, back_populates='fav_item')
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship(Course)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
