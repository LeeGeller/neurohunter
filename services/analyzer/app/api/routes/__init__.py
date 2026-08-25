from .vacancies.vacancies import router as vacancies_router
from .auth.auth import router as auth_router

routers = [
    vacancies_router,
    auth_router,
]
