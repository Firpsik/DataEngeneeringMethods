-- Create unstructured source table (with anomalies)
create schema if not exists s_psql_dds;

drop table if exists s_psql_dds.t_sql_source_unstructured cascade;

create table s_psql_dds.t_sql_source_unstructured (
    record_id integer,
    customer_name text,
    product_category text,
    city text,
    status text,
    payment_method text,
    amount numeric,
    quantity integer,
    discount_percent numeric,
    transaction_date date,
    rating numeric
);

comment on table s_psql_dds.t_sql_source_unstructured is 'Unstructured source table with raw data containing anomalies';
comment on column s_psql_dds.t_sql_source_unstructured.record_id is 'Record identifier (may contain duplicates)';
comment on column s_psql_dds.t_sql_source_unstructured.customer_name is 'Customer name (may contain nulls and formatting issues)';
comment on column s_psql_dds.t_sql_source_unstructured.product_category is 'Product category (may contain inconsistencies)';
comment on column s_psql_dds.t_sql_source_unstructured.city is 'City name (may contain nulls and case issues)';
comment on column s_psql_dds.t_sql_source_unstructured.status is 'Record status (may contain invalid values)';
comment on column s_psql_dds.t_sql_source_unstructured.payment_method is 'Payment method (may contain nulls)';
comment on column s_psql_dds.t_sql_source_unstructured.amount is 'Transaction amount (may be negative or null)';
comment on column s_psql_dds.t_sql_source_unstructured.quantity is 'Quantity (may be negative or zero)';
comment on column s_psql_dds.t_sql_source_unstructured.discount_percent is 'Discount percentage (may be out of range)';
comment on column s_psql_dds.t_sql_source_unstructured.transaction_date is 'Transaction date (may be null or future date)';
comment on column s_psql_dds.t_sql_source_unstructured.rating is 'Rating (may be out of range 1-5)';
