-- Таблица фактов (витрина данных)
create table if not exists s_psql_dds.t_dm_task (
    record_id integer not null,
    customer_id integer not null,
    product_category_id integer not null,
    city_id integer not null,
    status_id integer not null,
    payment_method_id integer not null,
    amount numeric(15, 2) not null,
    quantity integer not null,
    discount_percent numeric(5, 2) not null,
    transaction_date date not null,
    rating numeric(3, 1) not null,
    load_timestamp timestamp default current_timestamp,
    constraint t_dm_task_pk primary key (record_id, transaction_date),
    constraint fk_customer foreign key (customer_id) references s_psql_dds.d_customer(id),
    constraint fk_category foreign key (product_category_id) references s_psql_dds.d_product_category(id),
    constraint fk_city foreign key (city_id) references s_psql_dds.d_city(id),
    constraint fk_status foreign key (status_id) references s_psql_dds.d_status(id),
    constraint fk_payment foreign key (payment_method_id) references s_psql_dds.d_payment_method(id)
);

comment on table s_psql_dds.t_dm_task is 'Таблица фактов с ID из справочников';
comment on column s_psql_dds.t_dm_task.record_id is 'Идентификатор записи';
comment on column s_psql_dds.t_dm_task.customer_id is 'ID клиента из справочника';
comment on column s_psql_dds.t_dm_task.product_category_id is 'ID категории продукта из справочника';
comment on column s_psql_dds.t_dm_task.city_id is 'ID города из справочника';
comment on column s_psql_dds.t_dm_task.status_id is 'ID статуса из справочника';
comment on column s_psql_dds.t_dm_task.payment_method_id is 'ID способа оплаты из справочника';
comment on column s_psql_dds.t_dm_task.amount is 'Сумма транзакции';
comment on column s_psql_dds.t_dm_task.quantity is 'Количество';
comment on column s_psql_dds.t_dm_task.discount_percent is 'Процент скидки';
comment on column s_psql_dds.t_dm_task.transaction_date is 'Дата транзакции';
comment on column s_psql_dds.t_dm_task.rating is 'Рейтинг';
comment on column s_psql_dds.t_dm_task.load_timestamp is 'Время загрузки записи';

-- Индексы для оптимизации запросов
create index if not exists idx_t_dm_task_date on s_psql_dds.t_dm_task(transaction_date);
create index if not exists idx_t_dm_task_customer on s_psql_dds.t_dm_task(customer_id);
create index if not exists idx_t_dm_task_category on s_psql_dds.t_dm_task(product_category_id);
