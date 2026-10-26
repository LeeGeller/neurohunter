"""update work format constraints

Revision ID: f1f53c41bc5b
Revises: 824c017753b0
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "f1f53c41bc5b"
down_revision: Union[str, Sequence[str], None] = "824c017753b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


DEFAULT_WORK_FORMAT_CONSTRAINTS = {
    "remote": None,
    "office": None,
    "hybrid": None,
}


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "user_profiles",
        sa.Column(
            "work_format_constraints",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )

    op.execute(
        """
        UPDATE user_profiles
        SET work_format_constraints =
            '{"remote": null, "office": null, "hybrid": null}'::jsonb
        WHERE work_format_constraints IS NULL
        """
    )

    op.alter_column(
        "user_profiles",
        "work_format_constraints",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        nullable=False,
    )

    op.alter_column(
        "user_profiles",
        "preferred_work_days_per_week",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=True,
    )

    op.drop_column(
        "user_profiles",
        "preferred_work_formats",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.add_column(
        "user_profiles",
        sa.Column(
            "preferred_work_formats",
            postgresql.ARRAY(sa.VARCHAR()),
            nullable=True,
        ),
    )

    op.alter_column(
        "user_profiles",
        "preferred_work_days_per_week",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=True,
        postgresql_using="preferred_work_days_per_week::integer",
    )

    op.drop_column(
        "user_profiles",
        "work_format_constraints",
    )
