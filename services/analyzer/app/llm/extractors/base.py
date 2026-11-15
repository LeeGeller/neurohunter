"""Base extractor."""

import json
from typing import (
    Any,
    Generic,
    Optional,
    TypeVar,
    Union,
)

from pydantic import (
    BaseModel,
)

from app.llm.client import (
    OllamaClient,
)

T = TypeVar('T')


class BaseExtractor(Generic[T]):
    """BaseExtractor."""

    def __init__(
        self,
        llm_client: OllamaClient,
        response_model: Optional[type[BaseModel]]=None,
        response_schema: Optional[dict[str, Any]]=None,
    ) -> None:
        """Initialize."""

        self.llm_client = llm_client
        self.response_model = response_model
        self.response_schema = response_schema

        if response_model and response_schema:
            raise ValueError(
                'Pass either response_model or response_schema, not both'
            )

        self.response_schema = (
            response_model.model_json_schema()
            if response_model
            else response_schema
        )

    async def generate(self, promt: str) -> Union[T, dict[str, Any]]:
        """Generate."""

        response = await self.llm_client.generate(
            prompt=promt,
            response_schema=self.response_schema,
        )

        if self.response_model:
            return self.response_model.model_validate_json(response)

        return json.loads(response)
