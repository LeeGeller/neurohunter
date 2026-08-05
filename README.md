# NeuroHunter

**NeuroHunter** — Open Source-проект для сбора, структурированного анализа и персонализированной оценки вакансий с учётом особенностей восприятия, рабочей нагрузки и индивидуальных предпочтений пользователя.

Проект предназначен не только для поиска вакансий по профессиональным навыкам, но и для анализа условий работы:

- рабочий график;
- формат взаимодействия;
- уровень коммуникации;
- предсказуемость задач;
- когнитивная нагрузка;
- потенциальные риски перегрузки.

> Проект находится в активной разработке.

---

# Основная идея

Обычный поиск вакансий отвечает на вопрос:

> **«Подхожу ли я этой вакансии профессионально?»**

NeuroHunter должен дополнительно отвечать:

> **«Подходит ли эта вакансия мне как рабочая среда?»**

Для этого система разделяет анализ на несколько этапов:

```text
Источники вакансий
        ↓
Go Parsers
        ↓
MongoDB
        ↓
Python Analyzer
        ↓
LLM Feature Extraction
        ↓
VacancyFeatures
        ↓
User Profile
        ↓
Matching Algorithm
        ↓
VacancyMatch
```

---

# Текущий статус

## Этап 1. Сбор и хранение вакансий

* [x] Сбор вакансий на Go
* [x] Подготовка структуры проекта
* [x] Настройка Docker Compose
* [x] Подключение MongoDB
* [x] Хранение сырых данных вакансий

---

## Этап 2. Анализ вакансий

* [x] Подключение Python Analyzer
* [x] Получение вакансий из MongoDB
* [x] Подключение Ollama
* [x] Подключение локальной LLM Qwen3
* [x] Передача вакансии в модель
* [x] Создание модели `VacancyFeatures`
* [x] Извлечение структурированных признаков
* [x] Валидация результата через Pydantic
* [x] Добавление `evidence` для каждого результата
* [x] Первый интеграционный тест полного pipeline

---

## Этап 3. Профиль пользователя

### В работе

* [x] Проектирование модели `UserProfile`
* [x] Проектирование модели `UserFeatures`
* [ ] Настройка PostgreSQL
* [ ] Настройка SQLAlchemy
* [ ] Настройка Alembic
* [ ] Реализация регистрации пользователя
* [ ] Подтверждение email через токен
* [ ] Создание системы авторизации
* [ ] Реализация заполнения профиля пользователя
* [ ] Генерация пользовательских признаков

---

# Архитектура

Проект состоит из нескольких основных компонентов.

---

## Go Parser

Отвечает за сбор вакансий из внешних источников.

Основные задачи:

- получение вакансий;
- нормализация данных;
- извлечение базовых полей;
- сохранение данных.

Pipeline:

```text
Vacancy Source
      ↓
Go Parser
      ↓
MongoDB
```

---

## MongoDB

MongoDB используется для хранения исходных вакансий.

На этом этапе данные сохраняются максимально близко к оригинальному виду, чтобы не терять информацию для последующего анализа.

MongoDB хранит:

- описание вакансии;
- компанию;
- зарплату;
- формат работы;
- ссылку;
- исходные поля источника.

---

## Python Analyzer

Python-сервис отвечает за интеллектуальную обработку вакансий.

Основные задачи:

- получение вакансий из MongoDB;
- подготовка данных;
- отправка текста в LLM;
- получение структурированного результата;
- проверка через Pydantic.

---

# LLM Feature Extraction

Для анализа используется локальная LLM через [Ollama](https://ollama.com/).

Текущая модель:

```text
Qwen3 8B
```

LLM используется только для извлечения информации из текста вакансии.

Она не принимает окончательное решение:

> «Эта вакансия подходит пользователю».

Вместо этого она отвечает:

> «Какие характеристики есть у этой вакансии?»

Pipeline:

```text
Vacancy Description
        ↓
LLM
        ↓
VacancyFeatures
        ↓
Matching Algorithm
        ↓
VacancyMatch
```

---

# Модель данных

## Vacancy

Исходная модель вакансии:

```python
class Vacancy(BaseModel):
    id: str
    title: str
    vacancy_date: datetime
    description: str
    company: str
    work_location: str | None
    work_format: str | None
    salary_from: int | None
    salary_to: int | None
    currency: str | None
    url: str
```

---

## VacancyFeatures

`VacancyFeatures` содержит признаки, извлечённые из текста вакансии.

Пример:

```json
{
  "vacancy_id": "12345",

  "work_days_per_week": 5,
  "work_hours_per_day": 8,

  "flexible_schedule": false,

  "remote_possible": true,
  "office_required": false,

  "client_communication": true,
  "meeting_frequency": "daily",

  "multitasking_required": true,

  "task_predictability": null,

  "evidence": [
    "Работа 5/2 с 9:00 до 18:00",
    "Возможен удалённый формат",
    "Необходимо взаимодействие с клиентами"
  ]
}
```

Если данных недостаточно, система сохраняет:

```json
{
    "field": null
}
```

Это позволяет отличать:

- `true` — характеристика явно присутствует;
- `false` — характеристика отсутствует;
- `null` — информации недостаточно.

---

# Пользовательский профиль

NeuroHunter использует отдельную модель пользователя.

## UserProfile

Содержит данные, которые пользователь указывает самостоятельно:

```python
class UserProfile(BaseModel):

    age: int | None

    profession: str | None

    experience_years: float | None

    preferred_work_days_per_week: float | None

    preferred_work_hours_per_day: float | None

    flexible_schedule_needed: bool | None

    communication_preferences: str | None

    multitasking_tolerance: str | None

    deadline_tolerance: str | None

    preferred_team_size: str | None

    preferred_management_style: str | None

    conditions: list[str]

    about_me: str | None
```

---

## UserFeatures

После анализа профиля создаётся нормализованное представление пользователя:

```text
UserProfile
      ↓
Feature Extraction
      ↓
UserFeatures
```

`UserFeatures` используется системой сопоставления вакансий.

Примеры признаков:

- необходимый уровень коммуникации;
- предпочтительный график;
- чувствительность к перегрузке;
- потребность в предсказуемости задач;
- предпочтительный стиль управления.

---

# Персонализированная оценка

После появления пользовательского профиля система создаёт:

```python
class VacancyMatch(BaseModel):

    vacancy_id: str

    user_id: str

    profile_match: float

    skills_match: float

    experience_match: float

    work_format_match: float

    burnout_risk: float

    workload_risk: float

    social_overload_risk: float

    explanation: str
```

Pipeline:

```text
Vacancy
    ↓
VacancyFeatures

User
    ↓
UserFeatures

        ↓

Matching Algorithm

        ↓

VacancyMatch
```

---

# Почему анализ разделён на два этапа

NeuroHunter не использует LLM как "чёрный ящик", который принимает решения.

Система разделяет:

## 1. Извлечение информации

LLM отвечает:

> «Что известно о вакансии?»

Например:

- график;
- формат работы;
- уровень коммуникации;
- количество задач;
- требования.

---

## 2. Персональная оценка

Алгоритм отвечает:

> «Как эти условия подходят конкретному человеку?»

Это делает систему:

- более прозрачной;
- проверяемой;
- управляемой.

---

# Технологический стек

## Backend

- Go
- Python
- FastAPI
- Pydantic
- SQLAlchemy

## Data

- MongoDB
- PostgreSQL

## AI

- Ollama
- Qwen3 8B
- LLM Feature Extraction

## Infrastructure

- Docker
- Docker Compose

## Planned

- Redis
- Celery
- RAG
- Next.js
- TypeScript
- Tailwind CSS

---

# План развития

```text
[✓] Сбор вакансий
        ↓
[✓] Хранение вакансий
        ↓
[✓] Получение вакансий из MongoDB
        ↓
[✓] Подключение LLM
        ↓
[✓] Извлечение VacancyFeatures
        ↓
[✓] Pydantic validation
        ↓
[ ] Улучшение качества анализа
        ↓
[ ] PostgreSQL + Alembic
        ↓
[ ] Регистрация пользователей
        ↓
[ ] UserProfile
        ↓
[ ] UserFeatures
        ↓
[ ] VacancyMatch
        ↓
[ ] Оценка рисков нагрузки
        ↓
[ ] RAG
        ↓
[ ] Frontend
        ↓
[ ] Production deployment
```

---

# Цель проекта

NeuroHunter должен превратить поиск работы из простого поиска по ключевым словам в систему, которая учитывает реальные условия работы и индивидуальные особенности человека.

Главная идея:

> **Найти не просто работу, которую человек способен выполнять, а работу, в которой он сможет устойчиво работать.**

---

# Статус

Проект находится на стадии разработки MVP.

Текущий основной pipeline:

```text
Raw Vacancy
      ↓
Structured Vacancy
      ↓
LLM Feature Extraction
      ↓
VacancyFeatures
      ↓
User Profile
      ↓
VacancyMatch
```

Следующая ключевая задача — построение пользовательского слоя:

```text
Registration
      ↓
Authentication
      ↓
UserProfile
      ↓
UserFeatures
      ↓
Personalized Matching
```
