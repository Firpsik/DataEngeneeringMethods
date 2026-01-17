-- Create structured target table copy for testing
create schema if not exists s_psql_dds;

drop table if exists s_psql_dds.t_sql_source_structured_copy cascade;

create table s_psql_dds.t_sql_source_structured_copy (
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
    constraint t_sql_source_structured_copy_pk primary key (record_id, transaction_date)
);

comment on table s_psql_dds.t_sql_source_structured_copy is 'Copy of structured table for testing purposes';
