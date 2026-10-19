import uuid

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.postgres import (
    get_session,
)
from app.repositories.user_features_repository import (
    UserFeatureRepository,
    UserFeatureSearchResult,
)
from app.services.search_user_features import (
    SearchUserFeaturesService,
)

router = APIRouter(
    prefix='/internal/search',
    tags=['Internal Search'],
)


def get_search_user_features_service(
    session: AsyncSession = Depends(get_session),
) -> SearchUserFeaturesService:
    """Create search user features service."""

    repository = UserFeatureRepository(session)

    return SearchUserFeaturesService(repository)


@router.get(
    '/job-title-groups',
    status_code=status.HTTP_200_OK,
)
async def get_job_title_groups(
    service: SearchUserFeaturesService = Depends(
        get_search_user_features_service,
    ),
) -> dict[str, list[uuid.UUID]]:
    """Get job title groups with corresponding user IDs."""

    return await service.get_group_user_features_by_job_titles()


@router.get(
    '/user-features',
    status_code=status.HTTP_200_OK,
)
async def get_user_features(
    service: SearchUserFeaturesService = Depends(
        get_search_user_features_service,
    ),
) -> list[UserFeatureSearchResult]:
    """Get user features for search."""

    return await service.get_user_features()
