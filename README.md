# NeuroHunter

**NeuroHunter** — Open Source-сервис для анализа вакансий и оценки их соответствия конкретному кандидату.

Проект собирает вакансии, преобразует неструктурированные данные в структурированные характеристики с помощью LLM и создаёт основу для персонализированного подбора вакансий.

Главная идея NeuroHunter — перейти от обычного поиска вакансий по ключевым словам к системе, которая отвечает не только на вопрос:

> «Подхожу ли я этой вакансии?»

но и на вопрос:

> **«Насколько эта вакансия подходит именно мне?»**

Главная цель NeuroHunter:

> **Не найти как можно больше вакансий, а помочь понять, на какие вакансии действительно стоит откликаться — и почему.**

---

# Идея проекта

Обычные системы поиска вакансий в первую очередь ориентируются на совпадение:

```text
Vacancy requirements
        ↓
Candidate skills
        ↓
Match
```

NeuroHunter рассматривает соответствие с двух сторон:

```text
                    Vacancy
                       │
                       ▼
                VacancyFeatures
                       │
                       │
                       ▼
                 Matching Engine
                       ▲
                       │
                       │
                 UserFeatures
                       ▲
                       │
          ┌────────────┴────────────┐
          │                         │
     UserProfile             ResumeFeatures
```

### Профессиональное соответствие

Насколько профессиональные навыки и опыт кандидата соответствуют вакансии.

Например:

* Python;
* Django;
* PostgreSQL;
* опыт работы;
* профессиональные роли;
* проекты;
* другие технологии и компетенции.

### Рабочая совместимость

Насколько условия вакансии подходят конкретному человеку.

Например:

* график;
* формат работы;
* количество рабочих часов;
* командировки;
* клиентская коммуникация;
* многозадачность;
* количество встреч;
* уровень автономности;
* размер команды;
* стиль управления;
* социальная нагрузка;
* возможность профессионального роста.

Эти две стороны предполагается оценивать отдельно, чтобы пользователь мог понимать **не только насколько он подходит вакансии профессионально, но и насколько сама работа подходит ему**.

---

# Архитектура

```text
                         Habr Career
                              │
                              ▼
                      ┌──────────────┐
                      │  Go Parser   │
                      └──────┬───────┘
                             │
                             ▼
                      ┌──────────────┐
                      │   MongoDB    │
                      │ Raw Vacancies│
                      └──────┬───────┘
                             │
                             │
                             ▼
                      ┌──────────────┐
                      │    Python    │
                      │   Analyzer   │
                      └──────┬───────┘
                             │
                             ▼
                      ┌──────────────┐
                      │    Ollama    │
                      │   Qwen3:8B   │
                      └──────┬───────┘
                             │
                             ▼
                     ┌─────────────────┐
                     │ VacancyFeatures │
                     └────────┬────────┘
                              │
                              ▼
                       ┌────────────┐
                       │ PostgreSQL │
                       └────────────┘
                              │
                              ▼
                         FastAPI API
                              │
                              ▼
                            User
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
        UserProfile      UserFeatures    ResumeDocument
                                              │
                                              ▼
                                         ResumeFeatures
                                              │
                                              ▼
                                             LLM
```

---

# Основные компоненты

## Go Parser

Go-сервис отвечает за сбор вакансий.

Основные задачи:

* получение вакансий;
* парсинг страниц;
* извлечение данных вакансии;
* формирование raw vacancy;
* сохранение вакансий в MongoDB;
* предотвращение повторного создания одинаковых вакансий.

---

## MongoDB

MongoDB используется как хранилище исходных данных вакансий.

```text
Habr Career
     │
     ▼
Go Parser
     │
     ▼
MongoDB
     │
     ▼
Python Analyzer
```

Raw-данные сохраняются отдельно от результата анализа.

Это позволяет:

* повторно анализировать вакансии;
* менять prompt;
* менять модель;
* улучшать алгоритм анализа;
* не выполнять повторный парсинг источника.

---

# Python Analyzer

Python-сервис расположен в:

```text
services/analyzer/
```

Он отвечает за:

* API;
* работу с PostgreSQL;
* пользовательский слой;
* работу с MongoDB;
* LLM-интеграцию;
* извлечение структурированных признаков;
* валидацию данных;
* дальнейший matching.

Основной стек:

* FastAPI;
* SQLAlchemy;
* Alembic;
* Pydantic;
* PostgreSQL;
* MongoDB;
* Ollama;
* Qwen3:8B.

---

# Анализ вакансий

Текущий flow:

```text
Raw Vacancy
     │
     ▼
Python Analyzer
     │
     ▼
LLM
     │
     ▼
VacancyFeatures
     │
     ▼
Pydantic Validation
     │
     ▼
PostgreSQL
```

LLM используется не для хранения данных и не как основная бизнес-логика, а как слой преобразования неструктурированного текста в структурированную информацию.

Например, из текста вакансии могут извлекаться:

* рабочий график;
* количество рабочих дней;
* рабочие часы;
* формат работы;
* командировки;
* коммуникация;
* клиентское взаимодействие;
* многозадачность;
* требования;
* технологии;
* другие характеристики вакансии.

---

# Пользовательский слой

Пользовательская часть строится вокруг:

```text
User
 │
 ├── UserProfile
 │
 ├── UserFeatures
 │
 └── ResumeDocument
```

Между пользователем и каждой из моделей предусмотрена связь один-к-одному.

---

# UserProfile

`UserProfile` содержит подробное описание предпочтений и допустимых условий работы пользователя.

## Основная информация

* возраст;
* профессия;
* опыт работы;
* образование.

## Рабочие предпочтения

* количество рабочих дней в неделю;
* количество рабочих часов в день;
* гибкий график;
* переносимость переработок;
* предпочитаемое время окончания работы;
* работа в выходные;
* ночная работа;
* сменная работа;
* командировки.

## Коммуникация

* взаимодействие с клиентами;
* командная коммуникация;
* количество встреч;
* публичные выступления;
* телефонные звонки;
* клиентская поддержка;
* конфликтные ситуации.

## Организация задач

* многозадачность;
* дедлайны;
* переключение контекста;
* неопределённость;
* информационная нагрузка;
* количество прерываний.

## Рабочая среда

* предпочитаемый размер команды;
* стиль управления;
* структура задач;
* разнообразие задач;
* уровень автономности;
* частота обратной связи;
* переносимость шума;
* open-space.

## Формат работы

Профиль позволяет указывать предпочитаемые форматы работы.

Например:

* удалённая работа;
* гибрид;
* офис.

## Дополнительные факторы

* переносимость физической активности;
* работа стоя;
* поездки;
* факторы мотивации.

## Важность условий

Пользователь может задавать важность различных характеристик:

* доход;
* стабильность;
* интересные задачи;
* профессиональный рост;
* горизонтальный рост;
* вертикальный рост;
* автономность;
* гибкий график;
* work-life balance;
* удалённая работа;
* социальная среда;
* признание;
* значимость работы;
* разнообразие;
* творчество;
* другие факторы.

Также пользователь может добавить свободное описание в поле:

```text
about_me
```

---

# UserFeatures

`UserFeatures` — более компактное структурированное представление пользователя, предназначенное непосредственно для matching.

```text
UserFeatures
│
├── hard_constraints
├── preferences
├── tolerances
└── context
```

## `hard_constraints`

Жёсткие ограничения.

Условия, нарушение которых должно существенно влиять на возможность работы пользователя с вакансией.

Например:

```text
remote_only
no_business_trips
five_day_work_week
```

## `preferences`

Желательные условия.

Например:

```text
professional_growth
small_team
flexible_schedule
interesting_tasks
```

## `tolerances`

Условия, которые пользователь способен принять, даже если они не являются предпочтительными.

Это позволяет отличать:

```text
категорически неприемлемо
```

от:

```text
нежелательно, но допустимо
```

## `context`

Дополнительный контекст о пользователе, который может использоваться LLM при дальнейшем анализе.

---

# ResumeDocument

`ResumeDocument` хранит текущее резюме пользователя.

В отличие от первоначальной концепции `PortfolioDocument`, NeuroHunter **не хранит загруженный PDF или DOCX как файл**.

Файл используется только как транспорт для получения текста резюме.

Модель содержит:

```text
ResumeDocument
├── id
├── user_id
└── text
```

`user_id` уникален, поэтому у пользователя хранится только одно актуальное резюме.

При повторной загрузке старое резюме заменяется новым.

---

# Загрузка резюме

Поддерживаются:

* PDF;
* DOCX.

Flow:

```text
PDF / DOCX
     │
     ▼
FastAPI
     │
     ▼
ResumeTextExtractor
     │
     ├── PDF → pypdf
     │
     └── DOCX → python-docx
     │
     ▼
Plain Text
     │
     ▼
PostgreSQL
```

Оригинальный файл после извлечения текста не используется для хранения.

В PostgreSQL сохраняется только текст резюме.

Endpoint:

```http
POST /profile/resume
```

При повторной загрузке:

```text
Existing ResumeDocument
        ↓
      delete
        ↓
New ResumeDocument
```

---

# ResumeFeatures

Следующий уровень обработки резюме — преобразование текста в структурированные профессиональные признаки.

Flow:

```text
ResumeDocument
      │
      ▼
  resume.text
      │
      ▼
     LLM
      │
      ▼
ResumeFeatures
```

`ResumeFeatures` предназначен для извлечения профессиональной информации из резюме.

Текущая структура:

```text
ResumeFeatures
├── user_id
├── job_titles
├── hard_skills
├── soft_skills
├── experience
├── projects
├── weaknesses
├── strengths
└── experience_resume
```

### `job_titles`

Профессиональные должности и роли, указанные или подтверждённые опытом кандидата.

### `hard_skills`

Технологии, языки программирования, фреймворки, базы данных, инструменты и другие профессиональные навыки.

### `soft_skills`

Soft skills, которые явно указаны в резюме или непосредственно подтверждаются описанием профессионального опыта.

### `experience`

Общий профессиональный опыт в годах.

Например:

```text
2 года → 2.0
2 года 6 месяцев → 2.5
```

### `projects`

Проекты, явно указанные в резюме.

### `strengths`

Подтверждённые профессиональные сильные стороны.

### `weaknesses`

Только профессиональные слабые стороны, которые подтверждаются информацией резюме.

Система не должна придумывать недостатки на основании отсутствия информации.

### `experience_resume`

История профессионального опыта:

* должность;
* компания;
* период работы;
* задачи.

---

# LLM

Для локального анализа используется:

```text
Ollama
   ↓
Qwen3:8B
```

LLM работает локально и не требует передачи пользовательских резюме во внешний API.

Основной клиент находится в:

```text
services/analyzer/app/llm/client.py
```

Текущая архитектура отделяет:

```text
OllamaClient
     │
     ▼
Extractor
     │
     ▼
Structured Schema
```

Это позволяет отдельно тестировать:

* HTTP-взаимодействие с Ollama;
* prompt;
* extraction;
* JSON parsing;
* Pydantic validation.

---

# Отложенный анализ

NeuroHunter не предполагает обязательный запуск LLM при каждом поступлении вакансии.

Планируемая архитектура:

```text
              Continuous collection
                       │
                       ▼
                  Go Parser
                       │
                       ▼
                    MongoDB
                       │
                       │
                 scheduled batch
                       ▼
                    Queue
                       │
                       ▼
                   Ollama
                    Qwen3:8B
                       │
                       ▼
              Structured Features
                       │
                       ▼
                 PostgreSQL
```

Это позволяет:

* постоянно собирать новые вакансии;
* не запускать LLM для каждой вакансии сразу;
* обрабатывать накопленные данные пакетно;
* запускать тяжёлый анализ, например, один раз в сутки;
* отделить сбор данных от вычислительно затратного анализа.

Для очереди обработки планируется использовать Redis.

---

# Аутентификация

Пользовательский слой реализован на базе FastAPI Users.

Поддерживаются:

* регистрация;
* хеширование пароля;
* вход;
* JWT-аутентификация;
* получение текущего пользователя;
* подтверждение email;
* повторная отправка verification email.

Основные endpoints:

```http
POST /auth/register
POST /auth/login
POST /auth/request-verify-token
POST /auth/verify
GET  /auth/current-user
```

После регистрации:

```text
Registration
     │
     ▼
Verification JWT
     │
     ▼
Email
     │
     ▼
Verification
     │
     ▼
is_verified = true
```

Verification JWT не хранится в PostgreSQL как отдельная запись.

---

# PostgreSQL

PostgreSQL используется как основное структурированное хранилище.

В базе хранятся:

```text
users
user_profiles
user_features
resume_documents
vacancy_features
```

Связи пользовательского слоя:

```text
User
├── UserProfile
├── UserFeatures
└── ResumeDocument
```

Миграции управляются через Alembic.

```text
migrations/
└── versions/
```

---

# MongoDB

MongoDB используется для хранения исходных вакансий.

```text
Go Parser
    │
    ▼
MongoDB
    │
    ▼
Python Analyzer
```

MongoDB хранит raw vacancy data до её анализа и структурирования.

---

# Personalized Matching

Главная цель проекта — персонализированное сопоставление пользователя с вакансией.

Планируемый flow:

```text
                   UserProfile
                       │
                       ▼
                  UserFeatures
                       │
                       │
                       ▼
                 Matching Engine
                       ▲
                       │
                       │
                VacancyFeatures
                       ▲
                       │
                       ▼
                    Vacancy
```

В будущем результат может включать несколько независимых показателей.

Например:

```text
Professional fit:   82%
Work compatibility: 45%
```

Это позволит не сводить весь результат к одному числу и показывать пользователю, **почему вакансия подходит или не подходит**.

---

# Структура проекта

Текущая структура репозитория:

```text
neurohunter/
├── config/
├── core/
├── database/
├── handlers/
├── internal/
├── model/
│
├── services/
│   └── analyzer/
│       ├── app/
│       │   ├── api/
│       │   ├── config/
│       │   ├── database/
│       │   ├── llm/
│       │   ├── models/
│       │   ├── repositories/
│       │   ├── schemas/
│       │   ├── services/
│       │   ├── tests/
│       │   └── main.py
│       │
│       ├── migrations/
│       ├── utils/
│       ├── Dockerfile
│       ├── docker-compose.yml
│       ├── alembic.ini
│       └── pyproject.toml
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── go.mod
├── go.sum
├── main.go
└── README.md
```

Go-часть отвечает за сбор вакансий.

Python-сервис в `services/analyzer` отвечает за:

* API;
* анализ;
* LLM;
* PostgreSQL;
* пользовательский слой.

---

# Технологический стек

## Backend

* Python 3.13
* FastAPI
* FastAPI Users
* Pydantic
* SQLAlchemy
* Alembic

## Vacancy Parser

* Go
* goquery

## Databases

* PostgreSQL
* MongoDB

## LLM

* Ollama
* Qwen3:8B

## Resume Processing

* pypdf
* python-docx

## Infrastructure

* Docker
* Docker Compose
* Redis — планируется
* Nginx — планируется

---

# Текущий статус

## Этап 1. Сбор вакансий

### Завершено

* [x] Go-парсер
* [x] Получение вакансий
* [x] Парсинг данных вакансии
* [x] Формирование raw vacancy data
* [x] Подключение MongoDB
* [x] Хранение исходных вакансий
* [x] Защита от повторного создания одинаковых вакансий

### В работе

* [ ] Дополнительные источники вакансий
* [ ] Улучшение обработки ошибок
* [ ] Redis queue
* [ ] Отложенная пакетная обработка вакансий

---

# Этап 2. Анализ вакансий

### Завершено

* [x] Python Analyzer
* [x] Получение raw vacancy из MongoDB
* [x] Интеграция с Ollama
* [x] Передача вакансии в LLM
* [x] Анализ требований вакансии
* [x] Формирование `VacancyFeatures`
* [x] Pydantic validation
* [x] Сохранение результата в PostgreSQL
* [x] LLM extractor tests

### В работе

* [ ] Улучшение prompt
* [ ] Улучшение качества анализа
* [ ] Повторный анализ вакансий
* [ ] Batch processing
* [ ] Redis queue
* [ ] RAG

---

# Этап 3. Пользовательский слой

### Завершено

* [x] Пользовательская модель `User`
* [x] Регистрация пользователя
* [x] Хеширование пароля
* [x] JWT-аутентификация
* [x] Авторизация пользователя
* [x] Получение текущего пользователя
* [x] Email verification
* [x] Verification JWT
* [x] Отправка verification email
* [x] Подтверждение email
* [x] Проверка `is_verified`
* [x] Повторная отправка verification email
* [x] `UserProfile`
* [x] `UserFeatures`
* [x] Структура пользовательских предпочтений
* [x] Структура допустимых условий
* [x] Связь `User` → `UserProfile`
* [x] Связь `User` → `UserFeatures`
* [x] `ResumeDocument`
* [x] Связь `User` → `ResumeDocument`
* [x] PDF resume extraction
* [x] DOCX resume extraction
* [x] Сохранение извлечённого текста в PostgreSQL
* [x] Замена предыдущего резюме при повторной загрузке
* [x] `ResumeFeatures` schema
* [x] Resume LLM extractor
* [x] Resume extractor test
* [x] Подключение локальной Ollama из Docker

### В работе

* [ ] Улучшение resume prompt
* [ ] Повышение качества `ResumeFeatures`
* [ ] Сохранение `ResumeFeatures` в PostgreSQL
* [ ] End-to-end resume analysis flow
* [ ] Связывание resume features с vacancy matching
* [ ] Access / Refresh token flow

---

# Этап 4. Matching

### Планируется

* [ ] Matching Engine
* [ ] Professional fit
* [ ] Work compatibility
* [ ] Hard constraints validation
* [ ] Preferences matching
* [ ] Tolerances matching
* [ ] Explanation of matching results
* [ ] `VacancyMatch`
* [ ] Персонализированные рекомендации вакансий

---

# Этап 5. Infrastructure

### Планируется

* [ ] Redis
* [ ] Batch processing
* [ ] Scheduled analysis
* [ ] Nginx
* [ ] Production deployment
* [ ] Monitoring
* [ ] Logging
* [ ] Frontend

---

# Roadmap

```text
[✓] Go vacancy parser
        ↓
[✓] MongoDB raw storage
        ↓
[✓] Python analyzer
        ↓
[✓] Ollama / LLM integration
        ↓
[✓] VacancyFeatures
        ↓
[✓] Pydantic validation
        ↓
[✓] PostgreSQL
        ↓
[✓] SQLAlchemy
        ↓
[✓] Alembic
        ↓
[✓] User registration
        ↓
[✓] Email verification
        ↓
[✓] JWT authentication
        ↓
[✓] UserProfile
        ↓
[✓] UserFeatures
        ↓
[✓] User preferences and tolerances
        ↓
[✓] ResumeDocument
        ↓
[✓] PDF / DOCX text extraction
        ↓
[✓] Resume upload endpoint
        ↓
[~] ResumeFeatures extraction
        ↓
[~] Resume LLM quality
        ↓
[ ] ResumeFeatures persistence
        ↓
[ ] Batch LLM processing
        ↓
[ ] Redis
        ↓
[ ] VacancyMatch
        ↓
[ ] Professional fit
        ↓
[ ] Work compatibility
        ↓
[ ] RAG
        ↓
[ ] Frontend
        ↓
[ ] Nginx
        ↓
[ ] Production deployment
```

Обозначения:

```text
[✓] — реализовано
[~] — находится в разработке или требует дополнительного тестирования
[ ] — ещё не реализовано
```

---

# Запуск проекта

## Требования

Для локального запуска необходимы:

* Docker;
* Docker Compose;
* Go;
* Python;
* Poetry;
* Ollama;
* Qwen3:8B.

---

## Установка Python-зависимостей

```bash
cd services/analyzer

poetry install
```

---

## Запуск через Docker Compose

Из корня проекта:

```bash
docker compose up -d
```

Проверить контейнеры:

```bash
docker compose ps
```

Посмотреть логи API:

```bash
docker compose logs -f api
```

---

# Ollama

NeuroHunter использует локальную Ollama.

Проверить доступные модели:

```bash
ollama list
```

Ожидаемая модель:

```text
qwen3:8b
```

Поскольку Python Analyzer работает в Docker, а Ollama работает на host-машине, контейнер должен иметь доступ к host:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

Из контейнера Ollama доступна через:

```text
http://host.docker.internal:11434
```

---

# Миграции

Создание новой миграции:

```bash
docker compose exec api alembic revision --autogenerate -m "migration description"
```

Применение миграций:

```bash
docker compose exec api alembic upgrade head
```

Откат последней миграции:

```bash
docker compose exec api alembic downgrade -1
```

---

# Тестирование

Тесты Python Analyzer находятся в:

```text
services/analyzer/app/tests/
```

Запуск всех тестов:

```bash
docker compose exec api pytest
```

Запуск конкретного LLM-теста:

```bash
docker compose exec api pytest -s \
  app/tests/llm/test_extractor.py::test_resume_extract_features
```

LLM-тесты используют локальную Ollama.

---

# Environment variables

Основные переменные окружения:

```env
# PostgreSQL
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

# MongoDB
MONGO_URI=
MONGO_PORT=
MONGO_DB=
MONGO_USER=
MONGO_PASSWORD=

# Mongo Express
MONGO_EXPRESS_PORT=
MONGO_EXPRESS_USER=
MONGO_EXPRESS_PASSWORD=

# Go Parser
APP_PORT=

# Python Analyzer
ANALYZER_PORT=

# LLM
OLLAMA_HOST=
OLLAMA_MODEL=

# Email
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USER=
EMAIL_PASSWORD=
EMAIL_FROM=

EMAIL_VERIFICATION_URL=

# Authentication secrets
RESET_PASSWORD_TOKEN_SECRET=
VERIFICATION_TOKEN_SECRET=
AUTHENTICATION_SECRET=
```

Секретные значения не должны попадать в Git.

Для локальной разработки используется `.env`, а пример конфигурации хранится в:

```text
.env.example
```

---

# Принцип работы с пользовательскими данными

NeuroHunter разделяет:

```text
Raw data
    ↓
Structured data
    ↓
Matching
```

Для вакансий:

```text
Raw vacancy
    ↓
MongoDB
    ↓
LLM
    ↓
VacancyFeatures
    ↓
PostgreSQL
```

Для резюме:

```text
PDF / DOCX
    ↓
Text extraction
    ↓
ResumeDocument.text
    ↓
LLM
    ↓
ResumeFeatures
```

Оригинальный PDF/DOCX не хранится в PostgreSQL.

LLM не должен придумывать информацию, отсутствующую в исходных данных.

---

# Принципы LLM-анализа

LLM используется как инструмент структурирования данных.

Основные требования к анализу:

1. Использовать только информацию из исходного текста.
2. Не придумывать отсутствующие данные.
3. Не делать неподтверждённых предположений.
4. Разделять извлечение фактов и последующую оценку.
5. Валидировать структурированный результат через Pydantic.
6. Не использовать медицинские или психиатрические диагнозы для оценки кандидата.
7. Сохранять конкретные технологии и профессиональные факты.
8. Отделять пользовательские ограничения от предпочтений и допустимых условий.

---

# Open Source

NeuroHunter развивается как Open Source-проект.

Цель проекта — создать систему, которую можно:

* запустить локально;
* развернуть на собственном сервере;
* адаптировать под собственные требования;
* расширять новыми источниками вакансий;
* подключать к другим LLM;
* улучшать через собственные matching-алгоритмы.

В будущем проект предполагает возможность участия внешних contributors.

Pull Requests и предложения по улучшению приветствуются.

---
