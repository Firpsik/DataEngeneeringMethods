-- Справочник клиентов
create table if not exists s_psql_dds.d_customer (
    id serial primary key,
    name varchar(255) not null unique
);

comment on table s_psql_dds.d_customer is 'Справочник клиентов';
comment on column s_psql_dds.d_customer.id is 'Уникальный идентификатор клиента';
comment on column s_psql_dds.d_customer.name is 'Имя клиента';
