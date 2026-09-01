from app.api.routes.auth import router as auth_router
from app.api.routes.vacancies import router as vacancies_router
from app.api.routes.profile import router as profile_router

routers = [
    auth_router,
    vacancies_router,
    profile_router,
]
