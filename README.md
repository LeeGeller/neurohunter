# NeuroHunter

**NeuroHunter** — Open Source-сервис для персонализированного анализа вакансий.

Проект помогает ответить не только на вопрос:

> «Подхожу ли я вакансии?»

но и:

> «Подходит ли эта работа мне?»

Основная идея — разделять **профессиональное соответствие** и **рабочую совместимость**, чтобы пользователь видел не только итоговую оценку, но и причины, по которым вакансия подходит или не подходит.

---

## Архитектура

```text
                         Habr Career
                              │
                              ▼
                         Go Parser
                              │
                              ▼
                           MongoDB
                       Raw Vacancies
                              │
                    scheduled batch
                              │
                              ▼
                           Celery
                              │
                              ▼
                          RabbitMQ
                              │
                              ▼
                       LLM Worker
                              │
                              ▼
                        Ollama/Qwen
                              │
                              ▼
                       VacancyFeatures
                              │
                              ▼
                         PostgreSQL
                              │
                              ▼
                        Matching Engine
                              ▲
                 ┌────────────┴────────────┐
                 │                         │
           UserFeatures             ResumeFeatures
                 ▲                         ▲
                 │                         │
           UserProfile              ResumeDocument
```

Для пользовательских данных используется отдельный асинхронный flow:

```text
UserProfile / ResumeDocument
             │
             ▼
           Celery
             │
             ▼
          RabbitMQ
             │
             ▼
        LLM Worker
             │
             ▼
 UserFeatures / ResumeFeatures
```

Изменение исходных данных запускает повторный анализ.

---

## Основные компоненты

### Go Parser

Отвечает за сбор вакансий:

* получение вакансий;
* парсинг данных;
* формирование raw vacancy;
* сохранение в MongoDB;
* предотвращение дубликатов.

### MongoDB

Используется как хранилище исходных вакансий.

Raw-данные сохраняются отдельно от результатов анализа, поэтому вакансию можно повторно обработать после изменения prompt, модели или логики анализа.

### Python Analyzer

Находится в `services/analyzer/`.

Отвечает за:

* FastAPI API;
* PostgreSQL;
* пользовательский слой;
* LLM-интеграцию;
* извлечение структурированных признаков;
* дальнейший matching.

### Ollama / Qwen3:8B

LLM работает локально через Ollama.

Модель используется для преобразования неструктурированного текста в структурированные признаки.

### RabbitMQ + Celery

Используются для отложенного выполнения тяжёлых задач.

RabbitMQ отвечает за очередь сообщений, Celery — за выполнение задач.

Основные типы задач:

```text
UserFeatures
ResumeFeatures
VacancyFeatures
VacancyMatch
```

Это позволяет не выполнять LLM-анализ непосредственно во время HTTP-запроса.

---

## Пользовательский слой

```text
User
├── UserProfile
├── UserFeatures
└── ResumeDocument
```

### UserProfile

Содержит исходные предпочтения и допустимые условия работы пользователя:

* график;
* формат работы;
* рабочие часы;
* командировки;
* коммуникация;
* многозадачность;
* дедлайны;
* автономность;
* рабочая среда;
* мотивационные факторы;
* другие параметры и тд.

### UserFeatures

Структурированное представление пользователя для дальнейшего matching:

```text
UserFeatures
├── hard_constraints
├── preferences
├── tolerances
└── context
```

### ResumeDocument

Хранит текущее резюме пользователя.

Поддерживаются:

* PDF;
* DOCX.

Файл используется только для извлечения текста. Сам PDF/DOCX в PostgreSQL не хранится.

```text
PDF / DOCX
    ↓
Text extraction
    ↓
ResumeDocument.text
```

При повторной загрузке старое резюме заменяется новым.

Endpoint:

```text
POST /profile/resume
```

### ResumeFeatures

Извлекаются из текста резюме с помощью LLM.

Текущие признаки:

```text
ResumeFeatures
├── job_titles
├── hard_skills
├── soft_skills
├── experience
├── projects
├── weaknesses
├── strengths
└── experience_resume
```

---

## Анализ вакансий

Текущая концепция обработки:

```text
Raw Vacancy
     ↓
MongoDB
     ↓
batch
     ↓
Celery
     ↓
RabbitMQ
     ↓
LLM Worker
     ↓
VacancyFeatures
```

При этом не предполагается сохранять результаты анализа всех найденных вакансий.

Предварительный отбор должен уменьшать количество вакансий, которые проходят дорогой LLM-анализ и дальнейший matching.

---

## Matching

Целевая схема:

```text
UserFeatures
     │
ResumeFeatures
     │
     └──────────────┐
                    ▼
             Matching Engine
                    ▲
                    │
             VacancyFeatures
                    │
                    ▼
              VacancyMatch
```

Matching будет учитывать:

* профессиональное соответствие;
* рабочую совместимость;
* жёсткие ограничения;
* предпочтения;
* допустимые условия.

Результат планируется разделять как минимум на две независимые оценки:

```text
Professional fit
Work compatibility
```

---

# Технологический стек

### Backend

* Python 3.13
* FastAPI
* FastAPI Users
* Pydantic
* SQLAlchemy
* Alembic

### Vacancy Parser

* Go
* goquery

### Databases

* PostgreSQL
* MongoDB

### LLM

* Ollama
* Qwen3:8B

### Async processing

* Celery
* RabbitMQ

### Resume processing

* pypdf
* python-docx

### Infrastructure

* Docker
* Docker Compose

---

# Структура проекта

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
│       ├── alembic.ini
│       └── pyproject.toml
│
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── go.mod
├── go.sum
├── main.go
└── README.md
```

---

# Текущий статус

## Готово

### Vacancy Parser

* [x] Go parser
* [x] Получение вакансий
* [x] Парсинг данных
* [x] Raw vacancy
* [x] MongoDB
* [x] Защита от дубликатов

### Python Analyzer

* [x] FastAPI
* [x] PostgreSQL
* [x] SQLAlchemy
* [x] Alembic
* [x] MongoDB integration
* [x] Ollama integration
* [x] Qwen3:8B
* [x] LLM extractor
* [x] Pydantic validation
* [x] LLM tests

### Authentication

* [x] Registration
* [x] JWT authentication
* [x] Current user
* [x] Email verification
* [x] Verification JWT
* [x] Verification email

### User Profile

* [x] UserProfile
* [x] UserFeatures schema/model
* [x] User preferences
* [x] User tolerances
* [x] Hard constraints
* [x] User → UserProfile
* [x] User → UserFeatures

### Resume

* [x] ResumeDocument
* [x] PDF extraction
* [x] DOCX extraction
* [x] Resume upload endpoint
* [x] Raw text storage
* [x] Replacement of previous resume
* [x] ResumeFeatures schema
* [x] Resume LLM extractor
* [x] Resume extractor tests
* [x] Docker → host Ollama connection

### Infrastructure

* [x] Docker Compose
* [x] RabbitMQ container
* [x] Celery dependency
* [x] Celery worker container
* [x] Environment configuration for Celery/RabbitMQ

---

## В работе

### Resume analysis

* [ ] Улучшение ResumeFeatures prompt
* [ ] Повышение качества LLM-анализа
* [ ] Сохранение ResumeFeatures в PostgreSQL
* [ ] End-to-end flow:

```text
Resume upload
    ↓
ResumeDocument
    ↓
Celery
    ↓
RabbitMQ
    ↓
LLM
    ↓
ResumeFeatures
```

### Async processing

* [ ] Первый рабочий Celery task
* [ ] Подключение Celery worker к RabbitMQ
* [ ] UserFeatures processing
* [ ] ResumeFeatures processing
* [ ] Retry / error handling
* [ ] Idempotency задач
* [ ] Batch processing

---

# Планируется

## Vacancy pipeline

```text
Go Parser
    ↓
MongoDB
    ↓
Daily batch
    ↓
Celery
    ↓
RabbitMQ
    ↓
Vacancy analysis
    ↓
Minimum screening
    ↓
VacancyFeatures
```

Планируется анализировать и сохранять только вакансии, прошедшие предварительный отбор.

## Matching

* [ ] Matching Engine
* [ ] Professional fit
* [ ] Work compatibility
* [ ] Hard constraints
* [ ] Preferences
* [ ] Tolerances
* [ ] VacancyMatch
* [ ] Объяснение результатов
* [ ] Персонализированные рекомендации

## Infrastructure

* [ ] Scheduled jobs
* [ ] Monitoring
* [ ] Logging
* [ ] Nginx
* [ ] Production deployment
* [ ] Frontend

## Дополнительно

* [ ] RAG
* [ ] Дополнительные источники вакансий
* [ ] Улучшение обработки ошибок
* [ ] Access / Refresh token flow

---

# Запуск

## Требования

* Docker
* Docker Compose
* Go
* Python
* Poetry
* Ollama
* Qwen3:8B

Установка Python-зависимостей:

```bash
cd services/analyzer
poetry install
```

Запуск:

```bash
docker compose up -d --build
```

Проверка контейнеров:

```bash
docker compose ps
```

Логи API:

```bash
docker compose logs -f api
```

Логи Celery:

```bash
docker compose logs -f celery
```

---

## Ollama

NeuroHunter использует локальную Ollama.

Проверка модели:

```bash
ollama list
```

Ожидаемая модель:

```text
qwen3:8b
```

Ollama запускается на host-машине, поэтому Docker-контейнеры используют:

```text
http://host.docker.internal:11434
```

---

## Миграции

Создать миграцию:

```bash
docker compose exec api \
  alembic revision --autogenerate -m "migration description"
```

Применить:

```bash
docker compose exec api alembic upgrade head
```

Откатить последнюю:

```bash
docker compose exec api alembic downgrade -1
```

---

## Тестирование

Все тесты:

```bash
docker compose exec api pytest
```

Отдельный LLM-тест:

```bash
docker compose exec api pytest -s \
  app/tests/llm/test_extractor.py::test_resume_extract_features
```

LLM-тесты используют локальную Ollama.

---

## Environment

Основные переменные:

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

# Go Parser
APP_PORT=

# Python Analyzer
ANALYZER_PORT=

# RabbitMQ
RABBITMQ_AMQP_PORT=
RABBITMQ_MANAGEMENT_PORT=

# Celery
CELERY_BROKER_URL=

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

# Authentication
RESET_PASSWORD_TOKEN_SECRET=
VERIFICATION_TOKEN_SECRET=
AUTHENTICATION_SECRET=
```

Секретные значения не должны попадать в Git.

Для локальной разработки используется `.env`, пример конфигурации находится в `.env.example`.

---

# Roadmap

```text
[✓] Go Parser
      ↓
[✓] MongoDB
      ↓
[✓] Python Analyzer
      ↓
[✓] Ollama / Qwen3:8B
      ↓
[✓] VacancyFeatures foundation
      ↓
[✓] PostgreSQL / SQLAlchemy / Alembic
      ↓
[✓] Authentication
      ↓
[✓] UserProfile
      ↓
[✓] UserFeatures
      ↓
[✓] ResumeDocument
      ↓
[✓] PDF / DOCX extraction
      ↓
[✓] Celery + RabbitMQ infrastructure
      ↓
[~] ResumeFeatures
      ↓
[~] Async analysis flow
      ↓
[ ] Vacancy batch processing
      ↓
[ ] Vacancy screening
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

**Статус:** проект находится в активной разработке. Текущий фокус — завершение асинхронного LLM-пайплайна на базе **Celery + RabbitMQ**, после чего основной фокус сместится на персонализированный matching вакансий.
