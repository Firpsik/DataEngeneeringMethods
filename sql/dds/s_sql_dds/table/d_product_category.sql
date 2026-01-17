-- Справочник категорий продуктов
create table if not exists s_psql_dds.d_product_category (
    id serial primary key,
    name varchar(100) not null unique
);

comment on table s_psql_dds.d_product_category is 'Справочник категорий продуктов';
comment on column s_psql_dds.d_product_category.id is 'Уникальный идентификатор категории';
comment on column s_psql_dds.d_product_category.name is 'Название категории';
