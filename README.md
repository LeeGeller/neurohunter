# NeuroHunter

**NeuroHunter** — OpenSource-сервис для анализа IT-вакансий и оценки их соответствия особенностям и предпочтениям кандидата.

Проект анализирует вакансии с помощью LLM, структурирует полученные данные и в дальнейшем использует их для персонализированного matching.

---

## Архитектура

```text
                         ┌─────────────────┐
                         │   Habr Career   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │       Go        │
                         │     Parser      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     MongoDB     │
                         │   Raw Vacancies │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     Python      │
                         │     Analyzer    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │      LLM        │
                         │ Vacancy Analysis│
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    PostgreSQL   │
                         │ Structured Data │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     FastAPI     │
                         │       API       │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    Frontend     │
                         │      TODO       │
                         └─────────────────┘
```

---

# Структура проекта

```text
neurohunter/
├── parser/                  # Go-парсер вакансий
│
├── services/
│   └── analyzer/            # Python-сервис анализа
│       ├── app/
│       │   ├── api/          # API routes
│       │   ├── config/       # Configuration
│       │   ├── database/     # Database connections
│       │   ├── models/       # SQLAlchemy models
│       │   ├── schemas/      # Pydantic schemas
│       │   ├── services/     # Business logic
│       │   └── main.py
│       │
│       ├── migrations/       # Alembic migrations
│       ├── Dockerfile
│       ├── docker-compose.yml
│       ├── alembic.ini
│       └── pyproject.toml
│
└── README.md
```

---

# Технологический стек

## Parser

* Go
* goquery
* MongoDB

## Analyzer

* Python 3.13
* FastAPI
* FastAPI Users
* SQLAlchemy
* Alembic
* Pydantic
* PostgreSQL
* MongoDB
* Ollama / LLM
* FastAPI Mail

## Infrastructure

* Docker
* Docker Compose
* Nginx — планируется
* Redis — планируется

---

# Этап 1. Сбор вакансий

### Завершено

* [x] Go-парсер
* [x] Получение вакансий
* [x] Парсинг данных вакансии
* [x] Подготовка raw vacancy data
* [x] Подключение MongoDB
* [x] Хранение исходных вакансий
* [x] Защита от повторного создания одинаковых вакансий

### В работе

* [ ] Подключение дополнительных источников вакансий
* [ ] Улучшение обработки ошибок
* [ ] Очередь обработки вакансий через Redis

---

# Этап 2. Анализ вакансий

### Завершено

* [x] Python analyzer
* [x] Получение raw vacancy из MongoDB
* [x] Передача вакансии в LLM
* [x] Анализ требований вакансии
* [x] Формирование структурированного результата
* [x] Pydantic validation
* [x] Сохранение результата в PostgreSQL

### В работе

* [ ] Улучшение промптов
* [ ] Улучшение качества анализа
* [ ] Повторный анализ вакансий
* [ ] RAG

---

# Этап 3. Пользовательский слой

### Завершено

* [x] Проектирование пользовательской модели
* [x] Настройка PostgreSQL
* [x] Настройка SQLAlchemy
* [x] Настройка Alembic
* [x] Создание таблицы `users`
* [x] Регистрация пользователя
* [x] Хеширование пароля
* [x] JWT authentication
* [x] Авторизация пользователя
* [x] Получение текущего пользователя
* [x] Email verification
* [x] Генерация verification JWT
* [x] Отправка verification email
* [x] Подтверждение email
* [x] Проверка `is_verified`
* [x] Повторная отправка verification email

### В работе

* [ ] Access / Refresh tokens
* [ ] `UserProfile`
* [ ] `UserFeatures`
* [ ] Настройка пользовательских предпочтений
* [ ] Связывание пользователя с персонализированным matching

---

# Аутентификация

Пользовательский слой реализован с использованием `FastAPI Users`.

Текущий authentication flow:

```text
POST /auth/register
        │
        ▼
Создание User
        │
        ▼
Генерация verification JWT
        │
        ▼
Отправка email
        │
        ▼
POST /auth/verify
        │
        ▼
is_verified = true
        │
        ▼
POST /auth/login
        │
        ▼
JWT authentication
```

## Основные endpoints

```text
POST /auth/register
POST /auth/login
POST /auth/request-verify-token
POST /auth/verify
GET  /auth/current-user
```

### Регистрация

```http
POST /auth/register
```

Пример:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

После регистрации создаётся пользователь со следующими значениями:

```text
is_active = true
is_superuser = false
is_verified = false
```

---

## Email verification

После регистрации пользователь получает письмо с verification URL.

Verification token представляет собой JWT и не хранится в PostgreSQL как отдельная запись.

Секреты токенов хранятся в переменных окружения:

```text
RESET_PASSWORD_TOKEN_SECRET
VERIFICATION_TOKEN_SECRET
```

Процесс подтверждения:

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
User opens verification link
      │
      ▼
Frontend
      │
      ▼
POST /auth/verify
      │
      ▼
is_verified = true
```

На текущем этапе frontend ещё не реализован, поэтому endpoint `/auth/verify` тестируется напрямую через API.

После появления frontend verification URL будет вести на frontend-страницу, которая передаст token в:

```http
POST /auth/verify
```

---

# PostgreSQL

Основные данные приложения хранятся в PostgreSQL.

Текущая пользовательская таблица:

```text
users
├── id
├── email
├── hashed_password
├── is_active
├── is_superuser
└── is_verified
```

Verification JWT и reset-password JWT не хранятся в отдельных таблицах.

Миграции управляются через Alembic.

```text
migrations/
└── versions/
```

---

# MongoDB

MongoDB используется для хранения исходных данных вакансий.

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

# LLM Analysis

LLM используется для анализа вакансий и извлечения структурированных характеристик.

Общий flow:

```text
Raw Vacancy
     │
     ▼
LLM
     │
     ▼
Structured Vacancy Features
     │
     ▼
Pydantic validation
     │
     ▼
PostgreSQL
```

В дальнейшем результат анализа будет использоваться для персонализированного matching.

---

# Планируемая модель matching

Основная идея NeuroHunter — не просто искать вакансии по ключевым словам, а оценивать их соответствие конкретному пользователю.

Планируемый flow:

```text
User
 │
 ├── UserProfile
 │
 └── UserFeatures
          │
          ▼
   VacancyFeatures
          │
          ▼
   Matching Algorithm
          │
          ▼
    VacancyMatch
          │
          ▼
 Personalized Results
```

---

# Roadmap

```text
[✓] Go vacancy parser
        ↓
[✓] MongoDB raw storage
        ↓
[✓] Python analyzer
        ↓
[✓] LLM integration
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
[ ] UserProfile
        ↓
[ ] UserFeatures
        ↓
[ ] VacancyMatch
        ↓
[ ] RAG
        ↓
[ ] Frontend
        ↓
[ ] Redis
        ↓
[ ] Nginx
        ↓
[ ] Production deployment
```

---

# Development

Для запуска Python-сервиса используется Poetry.

```bash
poetry install
```

Запуск через Docker Compose:

```bash
docker compose up -d
```

Проверка контейнеров:

```bash
docker compose ps
```

Логи API:

```bash
docker compose logs -f api
```

---

# Database migrations

Создание новой миграции:

```bash
alembic revision --autogenerate -m "migration description"
```

Применение миграций:

```bash
alembic upgrade head
```

Откат последней миграции:

```bash
alembic downgrade -1
```

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
MONGO_DB=
MONGO_PORT=

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

# FastAPI Users
RESET_PASSWORD_TOKEN_SECRET=
VERIFICATION_TOKEN_SECRET=
```

Секретные значения не должны попадать в Git.

---

# Current status

На текущем этапе реализован основной backend foundation:

```text
Go
 │
 ▼
MongoDB
 │
 ▼
Python
 │
 ▼
LLM
 │
 ▼
PostgreSQL
 │
 ▼
FastAPI
 │
 ├── Registration
 ├── Login
 ├── JWT authentication
 ├── Email verification
 └── Current user
```

Следующий крупный этап — **пользовательский профиль и персонализированный matching вакансий**.

---

```
```
