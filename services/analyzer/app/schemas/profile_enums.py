"""User profile enums."""

from enum import (
    Enum,
)


class EducationLevel(str, Enum):
    """Education level enum."""

    SECONDARY_EDUCATION = 'Среднее образование'
    SPECIAL_EDUCATION = 'Специальное образование'
    HIGHTER_EDUCATION = 'Высшее образование'
    INCOMPLETE_HIGHER_EDUCATION = 'Незаконченное высшее образование'
    STUDENT_SPECIAL_EDUCATION = 'Студент специального образования'
    STUDENT_HIGHTER_EDUCATION = 'Студент высшего образования'


class OvertimeTolerance(str, Enum):
    """Overtime tolerance enum."""

    NEVER = 'Никогда'
    RARELY = 'Редко'
    SOMETIMES = 'Иногда'
    OFTEN = 'Часто'
    ALWAYS = 'Всегда'


class WeekendWork(str, Enum):
    """Weekend work enum."""

    USUALLY_WEEKENDS = 'Суббота и воскресенье'
    FLEXIBLE_DAYS_OFF = 'Плавающие выходные'
    WEEKENDS_ON_WEEKDAYS = 'Выходные в будние дни'


class NightWorkTolerance(str, Enum):
    """Night work tolerance enum."""

    NEVER = 'Никогда'
    RARELY = 'Редко'
    SOMETIMES = 'Иногда'
    OFTEN = 'Часто'
    ALWAYS = 'Всегда'

class ShiftWorkTolerance(str, Enum):
    """Tolerance to shift work.

    Describes how comfortable the user is with working
    according to a shift schedule with changing work hours.
    """

    NEVER = 'Не переношу вообще'
    LOW = 'Низкая'
    MEDIUM = 'Средняя'
    HIGH = 'Высокая'


class BusinessTripTolerance(str, Enum):
    """Tolerance to business trips.

    Describes how comfortable the user is with traveling for work.
    """

    NEVER = 'Не переношу вообще'
    LOW = 'Низкая'
    MEDIUM = 'Средняя'
    HIGH = 'Высокая'


class ClientCommunicationTolerance(str, Enum):
    """Tolerance to communication.

    Describes how comfortable the user is with different types of communication.
    """

    NEVER = 'Без общения'
    LOW_CLIENTS = 'Редкое общение, только с клиентами'
    RARE__CLIENTS = 'Редкое общение с клиентами, только по необходимости'
    MEDIUM_CLIENTS = 'Периодическое общение с клиентами, но не слишком часто'
    HIGH_CLIENTS = 'Частое общение, комфортно с клиентами'

class TeamCommunicationTolerance(str, Enum):
    """Tolerance to team communication.

    Describes how comfortable the user is with communicating with their team.
    """

    NEVER = 'Без общения'
    LOW_TEAM = 'Редкое общение, только с коллегами'
    RARE_TEAM = 'Редкое общение c коллегами, только по необходимости'
    MEDIUM_TEAM = 'Периодическое общение с коллегами, но не слишком часто'
    HIGH_TEAM = 'Частое общение, комфортно с командой'


class MeetingTolerance(str, Enum):
    """Tolerance to meetings.

    Describes how comfortable the user is with attending meetings.
    """

    NEVER = 'Без встреч'
    LOW_MEETINGS = 'Редкие встречи, только по необходимости'
    MEDIUM_MEETINGS = 'Периодические встречи, но не слишком часто'
    HIGH_MEETINGS = 'Частые встречи, комфортно с командой'


class PublicSpeakingTolerance(str, Enum):
    """Tolerance to public speaking.

    Describes how comfortable the user is with speaking in front of an audience.
    """

    NEVER = 'Без публичных выступлений'
    LOW_PUBLIC_SPEAKING = 'Редкие выступления, только по необходимости'
    MEDIUM_PUBLIC_SPEAKING = 'Периодические выступления, но не слишком часто'
    HIGH_PUBLIC_SPEAKING = 'Частые выступления, комфортно с аудиторией'


class PhoneCallTolerance(str, Enum):
    """Tolerance to phone calls.

    Describes how comfortable the user is with making and receiving phone calls.
    """

    NEVER = 'Работаю без звонков'
    COLD_CALLS_TRADER = 'Холодные звонки, продажи'
    COLD_CALLS = 'Холодные звонки приемлю, без продаж'
    WARM_CALLS_TRADER = 'Тёплые звонки, продажи'
    WARM_CALLS = 'Тёплые звонки, без продаж'
    HOT_CALLS_TRADER = 'Горячие звонки, продажи'
    HOT_CALLS = 'Горячие звонки, без продаж'


class CustomerSupportTolerance(str, Enum):
    """Tolerance to customer support work.

    Describes how comfortable the user is with work
    that involves helping customers, handling requests,
    solving problems, and responding to complaints.
    """

    NOT_ACCEPTABLE = 'Не подходит'
    DIFFICULT = 'Скорее не подходит'
    NEUTRAL = 'Нейтрально'
    ACCEPTABLE = 'Скорее подходит'
    PREFERRED = 'Предпочтительно'


class ConflictTolerance(str, Enum):
    """Tolerance to conflicts.

    Describes how comfortable the user is with handling conflicts,
    disagreements, and confrontations in the workplace.
    """

    AVOID = 'Избегаю конфликтов'
    LOW = 'Низкая толерантность к конфликтам'
    MEDIUM = 'Средняя толерантность к конфликтам'
    HIGH = 'Высокая толерантность к конфликтам'


class MultitaskingTolerance(str, Enum):
    """Tolerance to handling multiple tasks simultaneously."""

    SINGLE_TASK = 'Предпочитаю работать с одной задачей'
    FEW_TASKS = 'Могу работать с несколькими задачами'
    MANY_TASKS = 'Комфортно работаю с большим количеством задач'


class DeadlineTolerance(str, Enum):
    """Tolerance to deadlines.

    Describes how comfortable the user is with working under tight deadlines.
    """

    NEVER = 'Без дедлайнов'
    LOW = 'Низкая толерантность к дедлайнам'
    MEDIUM = 'Средняя толерантность к дедлайнам'
    HIGH = 'Высокая толерантность к дедлайнам'


class ContextSwitchingTolerance(str, Enum):
    """Tolerance to frequent switching between different tasks."""

    MINIMAL = 'Предпочитаю работать без частых переключений'
    OCCASIONAL = 'Нормально отношусь к периодическим переключениям'
    FREQUENT = 'Комфортно отношусь к частым переключениям'


class AmbiguityTolerance(str, Enum):
    """Tolerance to ambiguity.

    Describes how comfortable the user is with uncertainty,
    unclear instructions, and situations where information is incomplete.
    """

    AVOID = 'Предпочитаю чёткие инструкции и определённые задачи'
    LOW = 'Нужны в основном чёткие инструкции'
    MEDIUM = 'Могу работать при некоторой неопределённости'
    HIGH = 'Комфортно работаю при неопределённых требованиях'
    VERY_HIGH = 'Комфортно работаю в условиях высокой неопределённости'


class InformationOverloadTolerance(str, Enum):
    """Tolerance to information overload.

    Describes how comfortable the user is with processing large amounts of information.
    """

    AVOID = 'Предпочитаю работать с ограниченным объёмом информации'
    LOW = 'Нужны в основном структурированные и ограниченные данные'
    MEDIUM = 'Могу работать с умеренным объёмом информации'
    HIGH = 'Комфортно работаю с большим объёмом информации'


class InterruptionsTolerance(str, Enum):
    """Tolerance to interruptions.

    Describes how comfortable the user is with being interrupted during work.
    """

    AVOID = 'Предпочитаю работать без прерываний, либо если они редкие'
    LOW = 'Нужна в основном спокойная рабочая среда, редкие перерывы'
    MEDIUM = 'Нужно периодически прерываться от работы, но не слишком часто'
    HIGH = 'Часто прерываюсь во время работы, необходимы частые перерывы'


class BurnoutSensitivity(str, Enum):
    """Sensitivity to burnout.

    Describes how susceptible the user is to experiencing burnout.
    """

    LOW = 'Высокий порог выгорания, редко испытываю эмоциональное истощение'
    MEDIUM = 'При слишком интенсивной работе могу испытывать эмоциональное истощение'
    HIGH = 'Часто испытываю эмоциональное истощение, быстро выгораю'


class SocialOverloadSensitivity(str, Enum):
    """Sensitivity to social overload.

    Describes how susceptible the user is to experiencing social overload.
    """

    LOW = 'Высокий порог социальной перегрузки, комфортно общаюсь с людьми'
    MEDIUM = 'При слишком интенсивном общении могу испытывать социальную перегрузку'
    HIGH = 'Часто испытываю социальную перегрузку, быстро устаю от общения'


class PreferredTeamSize(str, Enum):
    """Preferred team size.

    Describes the user's preference for the size of the team they work with.
    """

    SOLO = 'Преимущественно самостоятельная работа'
    SMALL = 'Предпочитаю работать в маленькой команде (2-5 человек)'
    MEDIUM = 'Предпочитаю работать в средней команде (6-15 человек)'
    LARGE = 'Предпочитаю работать в большой команде (16+ человек)'


class PreferredManagementStyle(str, Enum):
    """Preferred management style.

    Describes the type of interaction and level of management
    the user prefers from their direct manager.
    """

    STRUCTURED = 'Чёткие задачи, правила и инструкции'
    SUPPORTIVE = 'Поддерживающий руководитель, к которому можно обратиться за помощью'
    AUTONOMOUS = 'Минимум контроля и высокая самостоятельность'
    COLLABORATIVE = 'Решения обсуждаются совместно'
    DIRECT = 'Прямые и конкретные указания'
    FLEXIBLE = 'Гибкий подход без жёстких правил'


class PreferredTaskStructure(str, Enum):
    """Preferred task structure.

    Describes how clearly tasks should be defined and structured
    before the user starts working on them.
    """

    HIGHLY_STRUCTURED = 'Чётко поставленные задачи с определёнными этапами'
    STRUCTURED = 'Понятные задачи с некоторой свободой действий'
    BALANCED = 'Баланс структуры и самостоятельности'
    FLEXIBLE = 'Гибко поставленные задачи с возможностью выбрать подход'
    OPEN_ENDED = 'Свободные задачи, где нужно самостоятельно определить способ решения'


class TaskVarietyPreference(str, Enum):
    """Preferred task variety.

    Describes how much variety the user prefers in their daily tasks.
    """

    REPETITIVE = 'Предпочитаю преимущественно однотипные задачи'
    MOSTLY_REPETITIVE = 'Предпочитаю в основном знакомые задачи с небольшим разнообразием'
    BALANCED = 'Предпочитаю баланс повторяющихся и разнообразных задач'
    MOSTLY_DIVERSE = 'Предпочитаю разнообразные задачи'
    HIGHLY_DIVERSE = 'Предпочитаю постоянное разнообразие задач'


class AutonomyLevel(str, Enum):
    """Preferred autonomy level.

    Describes how much independence the user prefers in their work.
    """

    LOW = 'Нужен постоянный контроль и руководство'
    MEDIUM = 'Нужна периодическая проверка и обратная связь'
    HIGH = 'Предпочитаю работать самостоятельно с минимальным контролем'


class FeedbackFrequencyPreference(str, Enum):
    """Preferred feedback frequency.

    Describes how often the user prefers to receive feedback
    about their work and progress.
    """

    AS_NEEDED = 'Только по необходимости'
    OCCASIONAL = 'Время от времени'
    REGULAR = 'Регулярно'
    FREQUENT = 'Очень часто'


class NoiseTolerance(str, Enum):
    """Tolerance to noise in the work environment.

    Describes how comfortable the user is with different levels
    of background noise while working.
    """

    VERY_LOW = 'Нужна практически тихая рабочая среда'
    LOW = 'Предпочитаю тихую рабочую среду'
    MEDIUM = 'Комфортно работаю при умеренном уровне шума'
    HIGH = 'Комфортно работаю при высоком уровне шума'


class OpenSpaceTolerance(str, Enum):
    """Tolerance to open-plan workspaces.

    Describes how comfortable the user is with working
    in an open office where multiple people share the same space.
    """

    VERY_LOW = 'Предпочитаю отдельное рабочее пространство'
    LOW = 'Скорее предпочитаю отдельный кабинет'
    MEDIUM = 'Могу работать как в отдельном кабинете, так и в open space'
    HIGH = 'Комфортно работаю в open space'


class WorkFormat(str, Enum):
    """Preferred work format."""

    REMOTE = 'Удалённая работа'
    HYBRID = 'Гибридная работа'
    OFFICE = 'Работа в офисе'


class PhysicalActivityTolerance(str, Enum):
    """Tolerance to physical activity in the workplace.

    Describes how comfortable the user is with work that requires
    different levels of physical effort.
    """

    NEVER = 'Без физической нагрузки'
    LOW = 'Минимальная физическая нагрузка'
    MEDIUM = 'Средняя физическая нагрузка'
    HIGH = 'Высокая физическая нагрузка'

class StandingWorkTolerance(str, Enum):
    """Tolerance to prolonged standing.

    Describes how comfortable the user is with work that requires
    spending extended periods of time standing or walking.
    """

    LOW = 'Предпочитаю работу преимущественно сидя'
    MEDIUM = 'Могу работать стоя или сидя в течение рабочего дня'
    HIGH = 'Комфортно работаю большую часть рабочего дня стоя'


class TravelTolerance(str, Enum):
    """Tolerance to work-related travel.

    Describes how comfortable the user is with traveling for work purposes.
    """

    NEVER = 'Без командировок'
    LOW = 'Редкие командировки, только по необходимости'
    MEDIUM = 'Периодические командировки, но не слишком часто'
    HIGH = 'Частые командировки, комфортно с поездками'


class MotivationFactor(str, Enum):
    """Factors that motivate the user at work.

    Describes the aspects of work that are important for the user's
    motivation and job satisfaction.
    """

    INCOME = 'Высокий доход'
    STABILITY = 'Стабильность и предсказуемость'
    INTERESTING_TASKS = 'Интересные и содержательные задачи'
    PROFESSIONAL_GROWTH = 'Профессиональное развитие'
    HORIZONTAL_CAREER_GROWTH = 'Горизонтальный карьерный рост'
    VERTICAL_CAREER_GROWTH = 'Вертикальный карьерный рост'
    AUTONOMY = 'Самостоятельность в работе'
    FLEXIBLE_SCHEDULE = 'Гибкий график'
    WORK_LIFE_BALANCE = 'Баланс работы и личной жизни'
    REMOTE_WORK = 'Возможность работать удалённо'
    SOCIAL_ENVIRONMENT = 'Комфортная рабочая атмосфера и отношения с коллегами'
    RECOGNITION = 'Признание результатов работы'
    MEANINGFUL_WORK = 'Ощущение пользы и смысла работы'
    VARIETY = 'Разнообразие задач'
    CREATIVITY = 'Возможность проявлять творческий подход'
    DMS = 'ДМС и социальные гарантии'
