-- Справочник способов оплаты
create table if not exists s_psql_dds.d_payment_method (
    id serial primary key,
    name varchar(50) not null unique
);

comment on table s_psql_dds.d_payment_method is 'Справочник способов оплаты';
comment on column s_psql_dds.d_payment_method.id is 'Уникальный идентификатор способа оплаты';
comment on column s_psql_dds.d_payment_method.name is 'Название способа оплаты';
