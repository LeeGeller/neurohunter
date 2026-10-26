from pydantic import (
    BaseModel,
    ConfigDict,
)


class WorkFormatConstraints(BaseModel):
    """Hard constraints for work formats."""

    model_config = ConfigDict(extra="forbid")

    remote: bool | None = None
    office: bool | None = None
    hybrid: bool | None = None
