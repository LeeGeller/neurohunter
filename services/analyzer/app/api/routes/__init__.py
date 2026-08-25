from .auth import auth_router
from .vacancies import vacancies_router

routers = [
    vacancies_router,
    auth_router,
]
