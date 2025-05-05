from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from course_app.db.models import StatusChoices, DaysChoices, RoleChoices, TypeChoices, Course


class UserProfileSchema(BaseModel):
    age: Optional[int]
    phone_number: Optional[str]
    profile_picture: Optional[str]
    bio_teacher: Optional[str]
    days: Optional[DaysChoices]
    status: Optional[StatusChoices]
    subject: Optional[str]
    experience: Optional[int]
    role: Optional[RoleChoices]
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True



class UserProfileLoginSchema(BaseModel):
    username: str
    password: str


    class Config:
        from_attributes = True



class NetworkCreateSchema(BaseModel):
    network_name: str
    title: Optional[str] = None
    user_id: int

class NetworkSchema(NetworkCreateSchema):
    id: int

    class Config:
        from_attributes = True



class CategorySchema(BaseModel):
    id: int
    category_name: str

    class Config:
        from_attributes = True



class CourseOutSchema(BaseModel):
    id: int
    course_name: str
    descriptions: str
    level: StatusChoices
    price: float
    type: TypeChoices
    course_certificate: bool
    category_id: int
    author_id: int
    created_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True


class CourseCreateSchema(BaseModel):
    course_name: str
    descriptions: str
    level: StatusChoices
    price: float
    type: TypeChoices
    course_certificate: bool
    category_id: int
    author_id: int

    class Config:
        from_attributes = True


class LessonOutSchema(BaseModel):
    id: int
    title: str
    video_url: Optional[str]
    video: Optional[str]
    content: Optional[str]
    course_id: int

    class Config:
        from_attributes = True


class LessonCreateSchema(BaseModel):
    title: str
    video_url: Optional[str]
    video: Optional[str]
    content: Optional[str]
    course_id: int

    class Config:
        from_attributes = True



class ExamOutSchema(BaseModel):
    id: int
    title: str
    end_time: datetime
    course_id: int

    class Config:
        from_attributes = True


class ExamCreateSchema(BaseModel):
    title: str
    end_time: datetime
    course_id: int

    class Config:
        from_attributes = True



class QuestionSchema(BaseModel):
    id: int
    title: str
    score: int
    exam_id: int

    class Config:
        from_attributes = True



class OptionSchema(BaseModel):
    id: int
    variant: str
    option_check: bool
    questions_id: int

    class Config:
        from_attributes = True



class AssignmentSchema(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    students_id: int

    class Config:
        from_attributes = True




class CertificateSchema(BaseModel):
    id: int
    certificate_url: str
    students_id: int
    course_id: int
    issued_at: datetime

    class Config:
        from_attributes = True




class CourseReviewSchema(BaseModel):
    id: int
    text: str
    stars: int
    course_id: int
    user_id: int

    class Config:
        from_attributes = True


class TeacherRatingSchema(BaseModel):
    id: int
    stars: int
    teacher_id: int

    class Config:
        from_attributes = True




class HistorySchema(BaseModel):
    id: int
    students_id: int
    course_id: int

    class Config:
        from_attributes = True



class CartItemSchema(BaseModel):
    course_id: int
    quantity: int


    class Config:
        from_attributes = True


class CartSchema(BaseModel):
    id: int
    user_id: int
    items: List[CartItemSchema] = []
    total_price: float

    class Config:
        from_attributes = True


class CartItemCreateSchema(BaseModel):
    course_id: int

    class Config:
        from_attributes = True



class FavoriteItemSchema(BaseModel):
    course_id: int
    quantity: int

    class Config:
        from_attributes = True


class FavoriteSchema(BaseModel):
    id: int
    user_id: int
    fav_item: List[FavoriteItemSchema] = []


    class Config:
        from_attributes = True


class FavoriteItemCreateSchema(BaseModel):
    course_id: int

    class Config:
        from_attributes = True
