-- Справочник статусов
create table if not exists s_psql_dds.d_status (
    id serial primary key,
    name varchar(50) not null unique
);

comment on table s_psql_dds.d_status is 'Справочник статусов';
comment on column s_psql_dds.d_status.id is 'Уникальный идентификатор статуса';
comment on column s_psql_dds.d_status.name is 'Название статуса';
