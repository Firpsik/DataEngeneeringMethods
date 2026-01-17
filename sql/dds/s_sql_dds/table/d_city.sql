-- Справочник городов
create table if not exists s_psql_dds.d_city (
    id serial primary key,
    name varchar(100) not null unique
);

comment on table s_psql_dds.d_city is 'Справочник городов';
comment on column s_psql_dds.d_city.id is 'Уникальный идентификатор города';
comment on column s_psql_dds.d_city.name is 'Название города';
