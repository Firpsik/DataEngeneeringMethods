-- Функция загрузки данных в витрину (Data Mart)
create or replace function s_psql_dds.fn_dm_data_load(
    start_dt date,
    end_dt date
)
returns integer
language plpgsql
as $$
declare
    rows_inserted integer := 0;
begin
    -- Заполнение справочников (если новые значения)
    
    -- Справочник клиентов
    insert into s_psql_dds.d_customer (name)
    select distinct customer_name
    from s_psql_dds.t_sql_source_structured
    where transaction_date between start_dt and end_dt
      and customer_name not in (select name from s_psql_dds.d_customer)
    on conflict (name) do nothing;
    
    -- Справочник категорий
    insert into s_psql_dds.d_product_category (name)
    select distinct product_category
    from s_psql_dds.t_sql_source_structured
    where transaction_date between start_dt and end_dt
      and product_category not in (select name from s_psql_dds.d_product_category)
    on conflict (name) do nothing;
    
    -- Справочник городов
    insert into s_psql_dds.d_city (name)
    select distinct city
    from s_psql_dds.t_sql_source_structured
    where transaction_date between start_dt and end_dt
      and city not in (select name from s_psql_dds.d_city)
    on conflict (name) do nothing;
    
    -- Справочник статусов
    insert into s_psql_dds.d_status (name)
    select distinct status
    from s_psql_dds.t_sql_source_structured
    where transaction_date between start_dt and end_dt
      and status not in (select name from s_psql_dds.d_status)
    on conflict (name) do nothing;
    
    -- Справочник способов оплаты
    insert into s_psql_dds.d_payment_method (name)
    select distinct payment_method
    from s_psql_dds.t_sql_source_structured
    where transaction_date between start_dt and end_dt
      and payment_method not in (select name from s_psql_dds.d_payment_method)
    on conflict (name) do nothing;
    
    -- Очистка целевой таблицы за период
    delete from s_psql_dds.t_dm_task
    where transaction_date between start_dt and end_dt;
    
    -- Загрузка данных с джойнами к справочникам
    insert into s_psql_dds.t_dm_task (
        record_id,
        customer_id,
        product_category_id,
        city_id,
        status_id,
        payment_method_id,
        amount,
        quantity,
        discount_percent,
        transaction_date,
        rating
    )
    select
        s.record_id,
        c.id as customer_id,
        pc.id as product_category_id,
        ct.id as city_id,
        st.id as status_id,
        pm.id as payment_method_id,
        s.amount,
        s.quantity,
        s.discount_percent,
        s.transaction_date,
        s.rating
    from s_psql_dds.t_sql_source_structured s
    inner join s_psql_dds.d_customer c on s.customer_name = c.name
    inner join s_psql_dds.d_product_category pc on s.product_category = pc.name
    inner join s_psql_dds.d_city ct on s.city = ct.name
    inner join s_psql_dds.d_status st on s.status = st.name
    inner join s_psql_dds.d_payment_method pm on s.payment_method = pm.name
    where s.transaction_date between start_dt and end_dt;
    
    get diagnostics rows_inserted = row_count;
    
    raise notice 'DM load completed: % rows inserted for period % to %', 
                 rows_inserted, start_dt, end_dt;
    
    return rows_inserted;
    
exception
    when others then
        raise exception 'DM load function failed: %', sqlerrm;
        return -1;
end;
$$;

comment on function s_psql_dds.fn_dm_data_load(date, date) is 
'Функция загрузки данных в витрину с заполнением справочников и джойном по ID';
