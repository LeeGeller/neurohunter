import asyncio

import httpx
from celery import (
    shared_task,
)

from app.config.settings import (
    settings,
)
from app.database.postgres import (
    get_session,
)


@shared_task
def search_vacancies(query: str) -> None:
    asyncio.run(
        _search_vacancies(
            query=query,
        ),
    )


async def _search_vacancies(query: str) -> None:
    """Search for vacancies based on the provided query."""

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'http://app:{settings.app_port}/search',
            params={'query': query},
        )
    response.raise_for_status()

    print(response.json())

