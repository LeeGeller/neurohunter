import json

import pytest

from app.config.settings import (
    settings,
)
from app.llm.client import (
    OllamaClient,
)
from app.llm.extractor import (
    ResumeFeaturesExtractor,
    VacancyFeaturesExtractor,
)
from app.models.vacancy import (
    Vacancy,
)
from app.models.vacancy_features import (
    VacancyFeatures,
)


@pytest.mark.asyncio
async def test_vacancy_extract_features():
    vacancy = Vacancy(
        id="12345",
        title="Python Developer",
        vacancy_date="2026-08-04T10:00:00",
        description="""
        Ищем Python-разработчика.

        Работа 5/2 с 9:00 до 18:00.
        Формат работы гибридный.
        Необходимо взаимодействовать с командой и заказчиками.
        Возможна работа над несколькими задачами одновременно.
        """,
        company="Test Company",
        work_location="Москва",
        work_format="hybrid",
        salary_from=150000,
        salary_to=200000,
        currency="RUB",
        url="https://example.com/vacancy/123",
    )

    llm_client = OllamaClient(
        base_url="http://host.docker.internal:11434",
        model=settings.ollama_model,
    )

    extractor = VacancyFeaturesExtractor(llm_client)

    try:
        features = await extractor.extract_features(vacancy)

        assert isinstance(features, VacancyFeatures)
        assert features.vacancy_id == vacancy.id
        assert features.work_days_per_week == 5
        assert features.work_hours_per_day == 8
        assert features.work_format == "hybrid"
        assert features.team_communication is True
        assert features.client_communication is True
        assert features.multitasking_required is True
        print("Extracted features:", features.dict())

    finally:
        await llm_client.close()


@pytest.mark.asyncio
async def test_resume_extract_features():

    resume = """
        БКА\n
        Женщина, 33 года, родилась 15 октября 1992\n
        +7 (999) 000-00-00 — предпочитаемый способ связи\n
        Проживает: Место проживания\n
        Гражданство: Россия, есть разрешение на работу: Россия\n
        Не готова к переезду, не готова к командировкам\n
        Желаемая должность и зарплата\n
        Backend-разработчик python\n
        Специализации:\n—  Программист, разработчик\n
        Тип занятости: полная занятость\n
        Формат работы: на месте работодателя, удалённо, гибрид\n
        Желательное время в пути до работы: не имеет значения\n
        Опыт работы — 2 года 1 месяц\n
        Сентябрь 2024 —\nнастоящее время\n2 года 1 месяц\n
        ООО Первая работа\n
        Младший разработчик\n
        Разработка внутренней CRM-системы для обучения, мониторинга и статистики по обучению\nперсонала\nОбразование
        \nНеоконченное высшее\n2019\nНеоконченное\nвысшее\nОмГМУ\nПедиатрический, Педиатрия\n
        Повышение квалификации, курсы\n2024 Python-разработчик\nSkypro, python-разработчик\n
        Навыки\nЗнание языков Русский — Родной\nАнглийский — B1 — Средний\n
        Навыки  Python      PostgreSQL      Linux      SQL      Docker      Redis      Git      API      REST \n
        GitHub      Django Framework      Django Rest Framework      Pytest      ООП      Flask \n
        Docker-compose      CI/CD      Unit Testing      Celery      REST API      JSON API      DR
        \n JWT      Bootstrap      Django \nРезюме обновлено 5 сентября 2026 в 19:02
        \nДополнительная информация\nОбо мне Я Python-разработчик с опытом в Django и DRF, работаю с backend-разработкой и базами
        \nданных. За 7 месяцев в компании успела плотно погрузиться в разработку CRM-системы для\n
        обучения сотрудников: API, авторизация, работа с данными, оптимизация запросов – всё это\nпро меня.
        \nСейчас хочу развиваться дальше, углубляться в проекты, писать более чистый код и\nпогружаться в процессы.
        Важна команда, где есть движение, обмен знаниями и можно реально\nрасти, а не просто \"делать задачи\".
        \nРабочие проекты:\n
        🛠 CRM для обучения – система управления обучением и аналитикой.\n
        🔹 Django, DRF – писала API, работала с сериализацией, авторизацией, ограничением прав.
        \n🔹 PostgreSQL – проектировала базу, писала запросы, оптимизировала.
        \nПет-проекты:\n📊 Парсер вакансий – собирает данные о вакансиях, анализирует.\n
        🔹 Telegram-бот – отправляет сообщения по расписанию через APScheduler.\n
        🔹 Парсинг – собирала вакансии, работала с BeautifulSoup, requests.\n
        🔹 Фоновые задачи – настраивала APScheduler для автоматического запуска.\n
        🔹 Docker – упаковывала проекты в контейнеры.\n
        🔹 Git – работаю с репозиториями, коммитами и базовыми командами.\n
        🔹 Linux – базовые команды.\nПроекты:\n
        Хочу работать с более сильной командой, где можно не только кодить, но и разбираться, почему\nименно так, обсуждать решения,
        получать конструктив и улучшать код.\n
        Soft-skills:\n🔹 Быстро подстраиваюсь под новые задачи и изменения в проекте.\n
        🔹 Открыта к новым подходам и не боюсь пробовать.\n
        🔹 Если чего-то не знаю – гуглю, спрашиваю, тестирую и нахожу решение, удивляюсь, когда\nлюди просто просят gpt написать за них, вместо того, чтобы разобрать \"под капотом\".\n
        🔹 Быстро обучаюсь, не боюсь задавать глупые вопросы. Но сначала ищу информацию сама.\n
        🔹 Чем больше конструктивной критики, тем лучше.\n
        🔹 Понимаю, что для компании важно не только красиво, но и быстро.\n
        Если ищете человека, которому реально горит, кто готов учиться и разбираться.
        \nGithub: https://github.com/LeeGeller\nБК •  Резюме обновлено 5 сентября 2026 в 19:02
    """

    llm_client = OllamaClient(
        base_url="http://host.docker.internal:11434",
        model=settings.ollama_model,
    )

    extractor = ResumeFeaturesExtractor(llm_client)

    try:
        features = await extractor.extract_features(resume)

        assert isinstance(features, dict)
        print(json.dumps(features, ensure_ascii=False, indent=4))

    finally:
        await llm_client.close()
