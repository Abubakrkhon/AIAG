# AI Tutor Agent

Профессиональный AI-агент для создания учебных материалов из любого контента.

## 🧠 Возможности

Агент принимает любой учебный контент и превращает его в:
- 📒 **Структурированный конспект** - кратко, логично, без воды
- 🧠 **Карточки Anki** - для интервального повторения (Q→A, Cloze)
- 📝 **Тесты и викторины** - multiple choice, клинические кейсы
- 🧩 **Схемы и диаграммы** - flowcharts, mind maps, таблицы
- 🎯 **Объяснения "на пальцах"** - для любого уровня (ребёнок, студент, эксперт)

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT LAYER                          │
│  PDF │ YouTube │ Audio │ Images │ DOCX │ TXT           │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                 PREPROCESSING LAYER                     │
│  Очистка │ Chunking │ Выделение терминов │ NLP         │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                    MEMORY SYSTEM                        │
│  Short-term (контекст) │ Long-term (Vector DB: FAISS)  │
│  User Memory (уровень знаний, слабые темы)              │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   CORE AGENTS                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │  Reader  │ │ Teacher  │ │ Examiner │ │   Anki   │  │
│  │  Agent   │ │  Agent   │ │  Agent   │ │  Agent   │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                    OUTPUT                               │
│  Конспект │ Карточки │ Тесты │ Схемы │ Объяснения     │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Быстрый старт

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Базовое использование

```python
from openai import OpenAI
from ai_tutor_agent import create_tutor, create_parsers

# Инициализация LLM клиента
client = OpenAI(api_key="your-api-key")
client.model = "gpt-4o-mini"

# Создание тьютора
tutor = create_tutor(client)

# Обработка текста
content = """
[Ваш учебный материал здесь...]
"""

results = tutor.process_content(content)

# Доступ к результатам
print(results['outputs']['summary']['content'])  # Конспект
print(results['outputs']['explanations'])        # Объяснения
print(results['outputs']['flashcards']['cards']) # Карточки
print(results['outputs']['tests']['questions'])  # Тесты
```

### Работа с файлами

```python
from ai_tutor_agent import create_parsers

parsers = create_parsers()

# PDF
pdf_result = parsers['pdf'].parse("lecture.pdf")
tutor.process_content(pdf_result['text'], pdf_result['metadata'])

# YouTube
yt_result = parsers['youtube'].parse("https://youtube.com/watch?v=...")
tutor.process_content(yt_result['text'], yt_result['metadata'])

# Аудио
audio_result = parsers['audio'].parse("lecture.mp3")
tutor.process_content(audio_result['text'], audio_result['metadata'])

# Изображения (OCR)
ocr_result = parsers['ocr'].parse("notes.jpg")
tutor.process_content(ocr_result['text'], ocr_result['metadata'])
```

## 🤖 Агенты системы

### Reader Agent
Читает и анализирует контент:
- Выделяет ключевые концепции
- Определяет термины и определения
- Оценивает сложность материала

### Teacher Agent
Объясняет концепции на разных уровнях:
- **Child** - как ребёнку (ELI5)
- **Beginner** - для начинающего
- **Intermediate** - для студента
- **Expert** - для продвинутого

### Examiner Agent
Создаёт тесты и оценки:
- Multiple choice вопросы
- Клинические/практические кейсы
- Проверка открытых ответов

### Anki Agent
Генерирует карточки для запоминания:
- Basic карты (Q→A)
- Cloze deletion (заполнить пропуск)
- Экспорт в .apkg формат

## 📁 Структура проекта

```
ai-tutor-agent/
├── agents/
│   ├── base_agent.py          # Базовый класс агента
│   ├── reader_agent.py        # Анализ контента
│   ├── teacher_agent.py       # Объяснения
│   ├── examiner_agent.py      # Тесты
│   ├── anki_agent.py          # Карточки Anki
│   └── orchestrator_agent.py  # Координация
├── core/
│   └── preprocessor.py        # Обработка текста
├── memory/
│   └── vector_memory.py       # Векторная память (FAISS)
├── parsers/
│   ├── pdf_parser.py          # PDF файлы
│   ├── youtube_parser.py      # YouTube видео
│   ├── audio_parser.py        # Аудио транскрипция
│   └── ocr_parser.py          # Распознавание изображений
├── config/
│   └── settings.py            # Конфигурация
└── utils/
    └── ...                    # Утилиты
```

## 🔧 Конфигурация

Создайте файл `.env`:

```env
AI_TUTOR_LLM_PROVIDER=openai
AI_TUTOR_LLM_MODEL=gpt-4o-mini
AI_TUTOR_LLM_API_KEY=your-api-key
AI_TUTOR_VECTOR_DB_TYPE=faiss
AI_TUTOR_CHUNK_SIZE=1000
AI_TUTOR_CHUNK_OVERLAP=200
```

## 📊 Примеры использования

### Медицинское образование

```python
# Создание клинического кейса
case = tutor.create_clinical_case(topic="Дифференциальный диагноз пневмонии")

# Генерация тестов с акцентом на клиническое мышление
tests = tutor.generate_tests(
    content=medical_text,
    question_count=20
)
```

### Подготовка к экзаменам

```python
# Создание полного набора материалов
results = tutor.process_content(textbook_chapter)

# Экспорт всех материалов
exported = tutor.export_all(
    output_dir="./exam_prep",
    formats=['md', 'json', 'apkg']
)
```

## 🛠️ Технологический стек

- **Backend**: Python 3.9+
- **LLM**: OpenAI GPT / Claude / Local LLM
- **NLP**: Whisper, tiktoken
- **Vector DB**: FAISS / Chroma
- **Parsers**: PyMuPDF, yt-dlp, pytesseract, OpenCV
- **API**: FastAPI (опционально)

## 📝 Лицензия

MIT License

## 🤝 Вклад

Contributions welcome! Please read CONTRIBUTING.md first.
