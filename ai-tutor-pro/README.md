# AI Tutor Pro - Профессиональная система обучения с ИИ

## 🌟 Обзор

**AI Tutor Pro** — это передовая платформа для трансформации любого учебного контента в интерактивные образовательные материалы с использованием искусственного интеллекта.

### 🔥 Ключевые возможности

#### 📥 Поддержка всех форматов ввода
- **PDF** — книги, статьи, методички (PyMuPDF + pdfplumber)
- **DOCX/TXT/MD** — текстовые документы
- **YouTube** — автоматическое скачивание и транскрибация (yt-dlp + Whisper)
- **Аудио** — лекции, подкасты, интервью (Whisper API)
- **Изображения** — фото конспектов, сканы (Tesseract OCR)
- **URL** — парсинг веб-страниц и статей

#### 🧠 Multi-Agent Архитектура
1. **Reader Agent** — интеллектуальный анализ контента
2. **Teacher Agent** — объяснения на 4 уровнях сложности
3. **Examiner Agent** — тесты, клинические кейсы, экзамены
4. **Anki Agent** — умные карточки с интервальным повторением
5. **Schema Agent** — визуальные схемы и ментальные карты
6. **Memory Agent** — долгосрочное хранение и контекст
7. **Orchestrator Agent** — координация всей системы

#### 🎯 Генерация материалов
- 📒 **Конспекты** — структурированные, без воды, с выделением главного
- 🧩 **Схемы** — flowchart, таблицы, mind-map, диаграммы
- 🧠 **Карточки Anki** — Q→A, Cloze, экспорт в .apkg
- 📝 **Тесты** — multiple choice, открытые вопросы, клинические кейсы
- 🎤 **Объяснения** — ELI5, Beginner, Intermediate, Expert уровни
- 📊 **План обучения** — персонализированный график повторений

#### 💎 Новые профессиональные функции
- **Real-time Chat** — диалог с ИИ по материалу
- **Progress Tracking** — аналитика обучения, слабые темы
- **Spaced Repetition** — алгоритм интервального повторения
- **Collaborative Mode** — совместная работа в группах
- **Voice Interface** — голосовое управление и ответы
- **Dark/Light Mode** — адаптивный дизайн
- **Multi-language** — поддержка 50+ языков
- **API Integration** — REST + WebSocket API
- **Export Options** — PDF, Markdown, Anki, Notion, Obsidian

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js 14)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Dashboard│ │  Editor  │ │  Chat    │ │ Analytics│       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
                            ↕ WebSocket/REST
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI + Python)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Gateway & Auth                       │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │               Multi-Agent System                      │   │
│  │  ┌────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐    │   │
│  │  │ Reader │ │ Teacher │ │ Examiner │ │  Anki    │    │   │
│  │  └────────┘ └─────────┘ └──────────┘ └──────────┘    │   │
│  │  ┌────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐    │   │
│  │  │ Schema │ │ Memory  │ │Orchestra-│ │ Progress │    │   │
│  │  │        │ │         │ │  tor     │ │          │    │   │
│  │  └────────┘ └─────────┘ └──────────┘ └──────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │PostgreSQL│ │  FAISS   │ │  Redis   │ │   S3     │       │
│  │(Users &) │ │(Vectors) │ │ (Cache)  │ │(Files)   │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Быстрый старт

### Требования
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

### Установка

#### 1. Бэкенд
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Отредактируйте .env с вашими API ключами
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Фронтенд
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

#### 3. Открыть в браузере
```
http://localhost:3000
```

## 📁 Структура проекта

```
ai-tutor-pro/
├── backend/
│   ├── agents/           # Multi-agent система
│   │   ├── base.py              # Базовый класс агента
│   │   ├── reader.py            # Анализ контента
│   │   ├── teacher.py           # Объяснения
│   │   ├── examiner.py          # Тесты и кейсы
│   │   ├── anki.py              # Карточки
│   │   ├── schema.py            # Схемы
│   │   ├── memory.py            # Управление памятью
│   │   └── orchestrator.py      # Координация
│   ├── parsers/          # Обработка входных данных
│   │   ├── pdf_parser.py
│   │   ├── youtube_parser.py
│   │   ├── audio_parser.py
│   │   ├── ocr_parser.py
│   │   └── web_parser.py
│   ├── memory/           # Системы памяти
│   │   ├── vector_store.py      # FAISS
│   │   ├── user_memory.py       # Профиль пользователя
│   │   └── cache.py             # Redis кэш
│   ├── api/              # API эндпоинты
│   │   ├── main.py              # FastAPI приложение
│   │   ├── routes/              # Маршруты
│   │   │   ├── upload.py
│   │   │   ├── process.py
│   │   │   ├── chat.py
│   │   │   ├── tests.py
│   │   │   └── analytics.py
│   │   └── middleware/          # Middleware
│   │       ├── auth.py
│   │       └── rate_limit.py
│   ├── utils/            # Утилиты
│   │   ├── llm_client.py        # LLM провайдеры
│   │   ├── text_processor.py    # Обработка текста
│   │   └── export.py            # Экспорт файлов
│   ├── models/           # SQLAlchemy модели
│   ├── schemas/          # Pydantic схемы
│   ├── config/           # Конфигурация
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/   # React компоненты
│   │   │   ├── ui/              # UI компоненты
│   │   │   ├── dashboard/       # Дашборд
│   │   │   ├── editor/          # Редактор
│   │   │   ├── chat/            # Чат
│   │   │   ├── cards/           # Карточки
│   │   │   ├── tests/           # Тесты
│   │   │   └── analytics/       # Аналитика
│   │   ├── pages/        # Страницы
│   │   ├── hooks/        # Custom hooks
│   │   ├── stores/       # Zustand stores
│   │   ├── styles/       # Глобальные стили
│   │   └── utils/        # Утилиты
│   ├── public/
│   ├── package.json
│   └── .env.example
│
├── docs/               # Документация
├── docker-compose.yml  # Docker конфигурация
├── README.md
└── LICENSE
```

## 🎨 Интерфейс

### Основные экраны

#### 🏠 Дашборд
- Статистика обучения
- Последние материалы
- Прогресс по темам
- Рекомендации

#### 📝 Редактор
- Загрузка файлов (drag & drop)
- Предпросмотр контента
- Настройки генерации
- Выбор типов вывода

#### 💬 Чат
- Диалог с ИИ по материалу
- Контекстная помощь
- Голосовой ввод
- История переписки

#### 📊 Аналитика
- Графики прогресса
- Слабые темы
- Время обучения
- Эффективность запоминания

#### 🧩 Карточки
- Режим обучения
- Статистика повторений
- Экспорт в Anki
- Создание своих карточек

#### 📝 Тесты
- Различные типы вопросов
- Таймер
- Мгновенная обратная связь
- Разбор ошибок

## 🔧 Технологический стек

### Backend
- **FastAPI** — современный async фреймворк
- **SQLAlchemy** — ORM
- **Pydantic** — валидация данных
- **FAISS** — векторный поиск
- **Redis** — кэширование
- **Celery** — фоновые задачи
- **OpenAI/Claude/Local LLM** — языковые модели
- **Whisper** — транскрибация

### Frontend
- **Next.js 14** — React фреймворк
- **TypeScript** — типизация
- **Tailwind CSS** — стилизация
- **Framer Motion** — анимации
- **Zustand** — state management
- **React Query** — data fetching
- **Socket.io** — real-time коммуникация
- **Recharts** — визуализация данных

### Infrastructure
- **Docker** — контейнеризация
- **PostgreSQL** — основная БД
- **Redis** — кэш и очереди
- **MinIO/S3** — хранение файлов
- **Nginx** — reverse proxy

## 📖 Примеры использования

### Python SDK

```python
from ai_tutor_pro import AITutor

# Инициализация
tutor = AITutor(api_key="your-key")

# Загрузка и обработка файла
result = await tutor.process_file(
    file_path="lecture.pdf",
    options={
        "generate_summary": True,
        "generate_flashcards": True,
        "generate_tests": True,
        "generate_schema": True,
        "explanation_level": "eli5"
    }
)

# Получение результатов
summary = result.summary
flashcards = result.flashcards
tests = result.tests
schema = result.schema

# Чат по материалу
response = await tutor.chat(
    message="Объясни механизм действия инсулина",
    context_id=result.context_id
)
```

### REST API

```bash
# Загрузка файла
curl -X POST http://localhost:8000/api/upload \
  -F "file=@lecture.pdf" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Запуск обработки
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "document_id": "doc_123",
    "options": {
      "summary": true,
      "flashcards": true,
      "tests": true
    }
  }'

# Чат
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "message": "Что такое гликолиз?",
    "context_id": "ctx_456"
  }'
```

## 🎯 Сценарии использования

### 🎓 Для студентов
- Конспектирование лекций
- Подготовка к экзаменам
- Изучение сложных тем
- Интервальное повторение

### 👨‍🏫 Для преподавателей
- Создание учебных материалов
- Генерация тестов
- Автоматизация проверки
- Аналитика успеваемости

### 🏥 Для медицинских студентов
- Клинические кейсы
- Дифференциальная диагностика
- Анатомические схемы
- Фармакологические карты

### 💼 Для профессионалов
- Повышение квалификации
- Изучение новой документации
- Быстрое освоение технологий
- Сертификационная подготовка

## 🔐 Безопасность

- JWT аутентификация
- Шифрование данных
- Rate limiting
- CORS политика
- Валидация входных данных
- Защита от инъекций

## 📈 Производительность

- Async обработка запросов
- Кэширование результатов
- Оптимизированные векторные поиски
- Горизонтальное масштабирование
- CDN для статики

## 🤝 Вклад в проект

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License — см. файл [LICENSE](LICENSE)

## 📞 Контакты

- Email: support@aitutorpro.com
- Telegram: @aitutorpro
- GitHub Issues: [Сообщить о проблеме](https://github.com/yourusername/ai-tutor-pro/issues)

---

**AI Tutor Pro** — Ваш персональный ИИ-наставник для эффективного обучения! 🚀
