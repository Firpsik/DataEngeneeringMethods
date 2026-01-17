-- Create structured target table (cleaned data)
create schema if not exists s_psql_dds;

drop table if exists s_psql_dds.t_sql_source_structured cascade;

create table s_psql_dds.t_sql_source_structured (
    record_id integer not null,
    customer_name varchar(255) not null,
    product_category varchar(100) not null,
    city varchar(100) not null,
    status varchar(50) not null,
    payment_method varchar(50) not null,
    amount numeric(15, 2) not null check (amount >= 0),
    quantity integer not null check (quantity > 0),
    discount_percent numeric(5, 2) not null check (discount_percent >= 0 and discount_percent <= 100),
    transaction_date date not null,
    rating numeric(3, 1) not null check (rating >= 1 and rating <= 5),
    load_timestamp timestamp default current_timestamp,
    constraint t_sql_source_structured_pk primary key (record_id, transaction_date)
);

comment on table s_psql_dds.t_sql_source_structured is 'Structured table with cleaned and validated data';
comment on column s_psql_dds.t_sql_source_structured.record_id is 'Unique record identifier';
comment on column s_psql_dds.t_sql_source_structured.customer_name is 'Cleaned customer name';
comment on column s_psql_dds.t_sql_source_structured.product_category is 'Standardized product category';
comment on column s_psql_dds.t_sql_source_structured.city is 'Standardized city name';
comment on column s_psql_dds.t_sql_source_structured.status is 'Valid status value';
comment on column s_psql_dds.t_sql_source_structured.payment_method is 'Payment method';
comment on column s_psql_dds.t_sql_source_structured.amount is 'Positive transaction amount';
comment on column s_psql_dds.t_sql_source_structured.quantity is 'Positive quantity';
comment on column s_psql_dds.t_sql_source_structured.discount_percent is 'Discount percentage (0-100)';
comment on column s_psql_dds.t_sql_source_structured.transaction_date is 'Valid transaction date';
comment on column s_psql_dds.t_sql_source_structured.rating is 'Rating (1-5)';
comment on column s_psql_dds.t_sql_source_structured.load_timestamp is 'Timestamp when record was loaded';

-- Create index for better query performance
create index idx_t_sql_source_structured_date on s_psql_dds.t_sql_source_structured(transaction_date);
create index idx_t_sql_source_structured_category on s_psql_dds.t_sql_source_structured(product_category);
