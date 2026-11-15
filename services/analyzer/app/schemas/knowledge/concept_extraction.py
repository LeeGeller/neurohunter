"""Schemas for professional concept extraction."""

from typing import (
    Literal,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ConceptSchema(BaseModel):
    """Represent an independently extracted professional concept."""

    model_config = ConfigDict(extra='forbid')

    source_text: str
    canonical_name: str


class ConceptOptionSchema(BaseModel):
    """Represent a concept within a logical group."""

    model_config = ConfigDict(extra='forbid')

    canonical_name: str


class ConceptGroupSchema(BaseModel):
    """Represent a group of concepts connected by a logical operator."""

    model_config = ConfigDict(extra='forbid')

    source_text: str
    operator: Literal['AND', 'OR']
    options: list[ConceptOptionSchema] = Field(
        default_factory=list,
    )


class ConceptExtractionSchema(BaseModel):
    """Represent the result of professional concept extraction."""

    model_config = ConfigDict(extra='forbid')

    concepts: list[ConceptSchema] = Field(
        default_factory=list,
    )
    concept_groups: list[ConceptGroupSchema] = Field(
        default_factory=list,
    )
