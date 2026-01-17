# Быстрый старт (Windows)

## Требования
- Python 3.11+
- Docker Desktop
- PostgreSQL

## Установка

```powershell
# 1. Клонировать репозиторий
git clone https://github.com/Firpsik/Methods.git
cd Methods

# 2. Создать виртуальное окружение
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Установить зависимости
pip install -r requirements.txt
```

## Запуск

### Вариант 1: Docker (рекомендуется)

```powershell
# Запустить PostgreSQL
docker-compose up -d postgres

# Подождать 10 секунд

# Запустить ETL
python data-pipeline/main.py
```

### Вариант 2: Локальная PostgreSQL

```powershell
# Создать базу данных (в psql)
CREATE DATABASE etl_database;

# Создать .env файл
Copy-Item env.example .env
# Отредактировать .env с вашими параметрами БД

# Запустить ETL
python data-pipeline/main.py
```

## Тестирование

```powershell
# Запустить все тесты
pytest data-pipeline/tests/ -v

# С покрытием кода
pytest data-pipeline/tests/ -v --cov=data-pipeline/src --cov-report=html

# Открыть отчет
start htmlcov/index.html
```

## Остановка

```powershell
# Остановить контейнеры
docker-compose down

# Удалить данные БД
docker-compose down -v
```

## Ожидаемый результат

```
ETL Pipeline Completed Successfully
Records generated: 1000
Records loaded to unstructured table: 1000
Records processed to structured table: ~400-500
```

```
Tests: 10 passed, 1 skipped
Code Coverage: 85%
```
