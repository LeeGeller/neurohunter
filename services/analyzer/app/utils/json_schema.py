"""JSON Schema generation from SQLAlchemy models."""

from sqlalchemy import (
    JSON,
    Boolean,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import (
    Float,
    Integer,
    String,
    Time,
)


def build_json_schema(model) -> dict:
    """Build JSON Schema from SQLAlchemy model."""

    properties = {}
    required = []

    for column in model.__table__.columns:
        column_type = column.type

        # Enum
        if isinstance(column_type, SQLEnum):
            field_schema = {
                "type": "string",
                "enum": column_type.enums,
            }

        # Boolean
        elif isinstance(column_type, Boolean):
            field_schema = {
                "type": "boolean",
            }

        # Integer
        elif isinstance(column_type, Integer):
            field_schema = {
                "type": "integer",
            }

        # Float
        elif isinstance(column_type, Float):
            field_schema = {
                "type": "number",
            }

        # Time
        elif isinstance(column_type, Time):
            field_schema = {
                "type": "string",
                "pattern": r"^\d{2}:\d{2}(:\d{2})?$",
            }

        # JSON
        elif isinstance(column_type, JSON):
            field_schema = {
                "type": "array",
                "items": {
                    "type": "string",
                },
            }

        # String
        elif isinstance(column_type, String):
            field_schema = {
                "type": "string",
            }

        else:
            raise TypeError(
                f"Unsupported column type: "
                f"{column.name} ({column_type})"
            )

        # Nullable fields
        if column.nullable:
            field_schema = {
                "anyOf": [
                    field_schema,
                    {"type": "null"},
                ]
            }

        properties[column.name] = field_schema
        required.append(column.name)

    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }
