"""Vacancy routes."""

from fastapi import (
    APIRouter,
    Request,
)

from app.repositories.vacancy_repository import (
    VacancyRepository,
)

router = APIRouter(
    prefix="/vacancies",
    tags=["Vacancies"],
)

@router.get("/")
async def get_vacancies(request: Request):
    """Get all vacancies."""
    db = request.app.state.mongo['neurohunter']

    repository = VacancyRepository(db)

    return await repository.get_all_vacancies()
