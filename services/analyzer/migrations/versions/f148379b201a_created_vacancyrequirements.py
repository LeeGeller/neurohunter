"""Created VacancyRequirements

Revision ID: f148379b201a
Revises: 9918032e1f46
Create Date: 2026-11-08 11:28:00.965056
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f148379b201a'
down_revision: Union[str, Sequence[str], None] = '9918032e1f46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Convert vacancy_id from VARCHAR to UUID.
    op.alter_column(
        'vacancy_features',
        'vacancy_id',
        existing_type=sa.VARCHAR(),
        type_=sa.UUID(),
        existing_nullable=False,
        postgresql_using='vacancy_id::uuid',
    )

    op.create_table(
        'vacancy_requirements',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('vacancy_id', sa.UUID(), nullable=False),
        sa.Column('mandatory_skills', sa.JSON(), nullable=True),
        sa.Column('preferred_skills', sa.JSON(), nullable=True),
        sa.Column('experience_min', sa.Float(), nullable=True),
        sa.Column('experience_max', sa.Float(), nullable=True),
        sa.Column('education_requirement', sa.String(), nullable=True),
        sa.Column('evidence', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(
            ['vacancy_id'],
            ['vacancy_features.vacancy_id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('vacancy_id'),
    )

    op.drop_column('user_profiles', 'experience_years')


def downgrade() -> None:
    """Downgrade schema."""

    # Drop dependent table first.
    op.drop_table('vacancy_requirements')

    # Convert vacancy_id back to VARCHAR.
    op.alter_column(
        'vacancy_features',
        'vacancy_id',
        existing_type=sa.UUID(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using='vacancy_id::varchar',
    )

    op.add_column(
        'user_profiles',
        sa.Column(
            'experience_years',
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
    )
