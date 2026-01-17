-- Целевая таблица в MySQL
create table if not exists s_sql_dm.t_dm_task (
    record_id int not null,
    customer_id int not null,
    customer_name varchar(255) not null,
    product_category_id int not null,
    product_category varchar(100) not null,
    city_id int not null,
    city varchar(100) not null,
    status_id int not null,
    status varchar(50) not null,
    payment_method_id int not null,
    payment_method varchar(50) not null,
    amount decimal(15, 2) not null,
    quantity int not null,
    discount_percent decimal(5, 2) not null,
    transaction_date date not null,
    rating decimal(3, 1) not null,
    load_timestamp timestamp default current_timestamp,
    primary key (record_id, transaction_date)
) engine=InnoDB default charset=utf8mb4 collate=utf8mb4_unicode_ci;

-- Индексы для оптимизации (MySQL не поддерживает IF NOT EXISTS для индексов)
-- create index idx_dm_task_date on s_sql_dm.t_dm_task(transaction_date);
-- create index idx_dm_task_customer on s_sql_dm.t_dm_task(customer_id);
-- create index idx_dm_task_category on s_sql_dm.t_dm_task(product_category_id);
