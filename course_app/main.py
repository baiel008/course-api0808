from fastapi import FastAPI
from course_app.api import (category, auth, course, network, lesson, cart,
                            Favorite, certificate, assignment, course_review,
                            exam, teacher_rating, history, option, question, social_auth)
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from course_app.admin.setup import setup_admin
from course_app.config import SECRET_KEYS


course_app = FastAPI()
course_app.include_router(category.category_router)
course_app.include_router(auth.auth_router)
course_app.include_router(course.course_router)
course_app.include_router(network.network_router)
course_app.include_router(lesson.lesson_router)
course_app.include_router(cart.cart_router)
course_app.include_router(Favorite.favorite_router)
course_app.include_router(certificate.certificate_router)
course_app.include_router(assignment.assignment_router)
course_app.include_router(course_review.course_review_router)
course_app.include_router(exam.exam_router)
course_app.include_router(teacher_rating.rating_router)
course_app.include_router(history.history_router)
course_app.include_router(option.option_router)
course_app.include_router(question.questions_router)
course_app.include_router(social_auth.social_router)
course_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEYS)
setup_admin(course_app)






if __name__ == '__main__':
    uvicorn.run(course_app, host='127.0.0.1', port=9999)