# COMMENT BOT FOR GGKIT

## Описание

Данный проект представляет собой Telegram-бота, предназначенного для автоматического размещения комментариев в канале.

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/khedamir/comment-bot.git
cd cd comment-bot
```

### 2. Создание и активация виртуального окружения

```bash
python -m venv venv
```

- **Windows**:

  ```bash
  venv\Scripts\activate
  ```

- **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск проекта

```bash
python bot.py
```

## Структура проекта

```plaintext
├── bot.py                 # Главный исполняемый файл
├── get_message.py         # Генерация комментария
├── process_new_post.py    # Отправка нового комментария
├── requirements.txt       # Файл зависимостей
└── README.md              # Документация проекта
```

## Требования

- Python 3.8+
- pip

## Автор

Автор: Kheda Amirova/GGKIT  
GitHub: khedamir
