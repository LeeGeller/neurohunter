from datetime import (
    datetime,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class Vacancy(BaseModel):
    """Vacancy model."""

    model_config = ConfigDict(
        populate_by_name=True,
    )

    id: str
    title: str
    vacancy_date: datetime = Field(alias="vacancydate")
    description: str
    company: str
    work_location: str | None = Field(alias="worklocation")
    work_format: str | None = Field(alias="workformat")
    salary_from: int | None = Field(alias="salaryfrom")
    salary_to: int | None = Field(alias="salaryto")
    currency: str | None
    url: str
