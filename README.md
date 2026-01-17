# Инструкция по запуску

## Требования
- Python 3.11+
- Docker Desktop

## Запуск

```powershell
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Запустить базы данных
docker-compose up -d postgres mysql

# 3. Подождать 15 секунд

# 4. Запустить пайплайн
python data-pipeline/main.py
```

## Результат

```
STEP 1: ETL Pipeline
✓ 1000 записей → 408 очищенных

STEP 2: PostgreSQL DWH
✓ Схема "звезда" создана
✓ 5 справочников заполнены

STEP 3: Заполнение витрины
✓ 408 записей в t_dm_task

STEP 4: MySQL Data Mart
✓ 408 записей загружено
```

## Проверка данных

### MySQL (основная витрина)
```powershell
docker exec etl-mysql mysql -u root -proot -e "SELECT COUNT(*) FROM s_sql_dm.t_dm_task;" 2>$null
docker exec etl-mysql mysql -u root -proot -e "SELECT * FROM s_sql_dm.t_dm_task LIMIT 5;" 2>$null
```

### PostgreSQL (DWH)
```powershell
docker exec etl-postgres psql -U postgres -d etl_database -c "SELECT * FROM s_psql_dds.d_customer LIMIT 5;"
docker exec etl-postgres psql -U postgres -d etl_database -c "SELECT * FROM s_psql_dds.d_product_category;"
```

## Остановка

```powershell
docker-compose down
```

## Архитектура

```
[Raw Data] 
    ↓ ETL
[PostgreSQL: t_sql_source_structured] 
    ↓ DM Load + Справочники
[PostgreSQL: t_dm_task + d_*] (схема "звезда")
    ↓ View: v_dm_task
[MySQL: t_dm_stg_task] 
    ↓ Процедура
[MySQL: t_dm_task] ← ФИНАЛЬНАЯ ВИТРИНА
```

## Что делает пайплайн

1. **Генерирует** 1000 записей с аномалиями
2. **Очищает** данные SQL-функцией
3. **Создает** справочники (клиенты, категории, города, статусы, платежи)
4. **Заполняет** таблицу фактов с FK на справочники
5. **Переносит** данные в MySQL для финальной витрины
