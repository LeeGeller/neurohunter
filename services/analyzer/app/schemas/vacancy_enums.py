"""Vacancy-specific enums."""

from enum import Enum


class VacancyFrequency(str, Enum):
    """Frequency of a requirement in a vacancy."""

    NONE = 'Нет'
    RARELY = 'Редко'
    SOMETIMES = 'Иногда'
    OFTEN = 'Часто'
    ALWAYS = 'Всегда'


class VacancyIntensity(str, Enum):
    """Intensity of a requirement in a vacancy."""

    NONE = 'Нет'
    LOW = 'Низкая'
    MEDIUM = 'Средняя'
    HIGH = 'Высокая'
