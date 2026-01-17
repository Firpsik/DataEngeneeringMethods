# Схема Data Warehouse (Звезда)

## Архитектура

```
                                    ┌─────────────────┐
                                    │  t_dm_task      │
                                    │  (FACT TABLE)   │
                                    ├─────────────────┤
                                    │ record_id (PK)  │
                                    │ transaction_date│
                ┌───────────────────│ customer_id (FK)│───────────────────┐
                │                   │ category_id (FK)│                   │
                │                   │ city_id (FK)    │                   │
                │     ┌─────────────│ status_id (FK)  │─────────────┐     │
                │     │             │ payment_id (FK) │             │     │
                │     │             │ amount          │             │     │
                │     │             │ quantity        │             │     │
                │     │             │ discount_%      │             │     │
                │     │             │ rating          │             │     │
                │     │             └─────────────────┘             │     │
                │     │                                             │     │
                ▼     ▼                                             ▼     ▼
         ┌──────────┐  ┌─────────────┐                  ┌──────────┐  ┌──────────┐
         │d_customer│  │d_product_   │                  │ d_city   │  │ d_status │
         │          │  │  category   │                  │          │  │          │
         ├──────────┤  ├─────────────┤                  ├──────────┤  ├──────────┤
         │ id (PK)  │  │ id (PK)     │                  │ id (PK)  │  │ id (PK)  │
         │ name     │  │ name        │                  │ name     │  │ name     │
         └──────────┘  └─────────────┘                  └──────────┘  └──────────┘
                                             
                              ┌───────────────┐
                              │d_payment_     │
                              │  method       │
                              ├───────────────┤
                              │ id (PK)       │
                              │ name          │
                              └───────────────┘
```

## Поток данных

```
┌──────────────────┐
│  Источник        │
│  (Raw Data)      │
└────────┬─────────┘
         │
         │ 1. ETL (fn_etl_data_load)
         │    Очистка аномалий
         ▼
┌────────────────────────┐
│  t_sql_source_         │
│  structured            │
│  (Cleaned Data)        │
└────────┬───────────────┘
         │
         │ 2. DM Load (fn_dm_data_load)
         │    Заполнение справочников
         │    Джойн по name → получение ID
         ▼
┌────────────────────────┐
│  t_dm_task + d_*       │
│  (PostgreSQL DWH)      │
│  Схема "Звезда"        │
└────────┬───────────────┘
         │
         │ 3. View (v_dm_task)
         │    Развертка с джойнами
         ▼
┌────────────────────────┐
│  v_dm_task             │
│  (Витрина PostgreSQL)  │
└────────┬───────────────┘
         │
         │ 4. ETL to MySQL
         │    Перекладка данных
         ▼
┌────────────────────────┐
│  t_dm_stg_task         │
│  (MySQL Staging)       │
└────────┬───────────────┘
         │
         │ 5. MySQL Proc (fn_dm_data_stg_to_dm_load)
         │    Загрузка в финальную таблицу
         ▼
┌────────────────────────┐
│  t_dm_task             │
│  (MySQL Data Mart)     │
└────────────────────────┘
```

## Справочники (Dimensions)

| Таблица | Описание | Пример данных |
|---------|----------|---------------|
| `d_customer` | Клиенты | Иванов Иван Иванович |
| `d_product_category` | Категории | Электроника, Одежда |
| `d_city` | Города | Москва, Казань |
| `d_status` | Статусы | Активный, Неактивный |
| `d_payment_method` | Способы оплаты | Карта, Наличные |

## Таблица фактов (Facts)

| Поле | Тип | Описание |
|------|-----|----------|
| `record_id` | INT | ID записи (PK) |
| `customer_id` | INT | FK → d_customer |
| `product_category_id` | INT | FK → d_product_category |
| `city_id` | INT | FK → d_city |
| `status_id` | INT | FK → d_status |
| `payment_method_id` | INT | FK → d_payment_method |
| `amount` | NUMERIC | Сумма транзакции |
| `quantity` | INT | Количество |
| `discount_percent` | NUMERIC | Скидка % |
| `transaction_date` | DATE | Дата (PK) |
| `rating` | NUMERIC | Рейтинг 1-5 |
