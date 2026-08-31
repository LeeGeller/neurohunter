from app.api.routes.auth import router as auth_router
from app.api.routes.vacancies import router as vacancies_router

routers = [
    auth_router,
    vacancies_router
]
