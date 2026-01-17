-- Test ETL function to transform and load data to copy table
create or replace function s_psql_dds.fn_etl_data_load_test(
    start_date date,
    end_date date
)
returns integer
language plpgsql
as $$
declare
    rows_inserted integer := 0;
begin
    -- Clear test table for the date range
    delete from s_psql_dds.t_sql_source_structured_copy
    where transaction_date between start_date and end_date;
    
    -- Insert cleaned and transformed data (same logic as main ETL)
    insert into s_psql_dds.t_sql_source_structured_copy (
        record_id,
        customer_name,
        product_category,
        city,
        status,
        payment_method,
        amount,
        quantity,
        discount_percent,
        transaction_date,
        rating
    )
    select
        record_id,
        initcap(trim(coalesce(customer_name, 'Unknown'))) as customer_name,
        case
            when lower(trim(coalesce(product_category, ''))) in ('электроника', 'elektronika') then 'Электроника'
            when lower(trim(coalesce(product_category, ''))) in ('одежда', 'odezhda') then 'Одежда'
            when lower(trim(coalesce(product_category, ''))) in ('продукты', 'produkty') then 'Продукты'
            when lower(trim(coalesce(product_category, ''))) in ('мебель', 'mebel') then 'Мебель'
            when lower(trim(coalesce(product_category, ''))) in ('книги', 'knigi') then 'Книги'
            else 'Прочее'
        end as product_category,
        initcap(trim(coalesce(city, 'Unknown'))) as city,
        case
            when lower(trim(coalesce(status, ''))) in ('активный', 'active') then 'Активный'
            when lower(trim(coalesce(status, ''))) in ('неактивный', 'inactive') then 'Неактивный'
            when lower(trim(coalesce(status, ''))) in ('приостановлен', 'suspended') then 'Приостановлен'
            else 'Неактивный'
        end as status,
        coalesce(payment_method, 'Не указан') as payment_method,
        case
            when amount is null then 0
            when amount < 0 then abs(amount)
            when amount > 1000000 then 1000000
            else amount
        end as amount,
        case
            when quantity is null or quantity <= 0 then 1
            else quantity
        end as quantity,
        case
            when discount_percent is null then 0
            when discount_percent < 0 then 0
            when discount_percent > 100 then 100
            else discount_percent
        end as discount_percent,
        case
            when transaction_date is null then current_date
            when transaction_date > current_date then current_date
            else transaction_date
        end as transaction_date,
        case
            when rating is null then 3.0
            when rating < 1 then 1.0
            when rating > 5 then 5.0
            else rating
        end as rating
    from (
        select distinct on (record_id, transaction_date)
            record_id,
            customer_name,
            product_category,
            city,
            status,
            payment_method,
            amount,
            quantity,
            discount_percent,
            transaction_date,
            rating
        from s_psql_dds.t_sql_source_unstructured
        where 
            case
                when transaction_date is null then current_date
                when transaction_date > current_date then current_date
                else transaction_date
            end between start_date and end_date
        order by record_id, transaction_date, ctid
    ) as deduplicated;
    
    get diagnostics rows_inserted = row_count;
    
    raise notice 'Test ETL completed: % rows inserted into test table for date range % to %', 
                 rows_inserted, start_date, end_date;
    
    return rows_inserted;
    
exception
    when others then
        raise exception 'Test ETL function failed: %', sqlerrm;
        return -1;
end;
$$;

comment on function s_psql_dds.fn_etl_data_load_test(date, date) is 
'Test ETL function to clean and transform data to copy table for testing purposes';
