-- ETL function to transform and load data from unstructured to structured table
create or replace function s_psql_dds.fn_etl_data_load(
    start_date date,
    end_date date
)
returns integer
language plpgsql
as $$
declare
    rows_inserted integer := 0;
begin
    -- Clear structured table for the date range
    delete from s_psql_dds.t_sql_source_structured
    where transaction_date between start_date and end_date;
    
    -- Insert cleaned and transformed data
    insert into s_psql_dds.t_sql_source_structured (
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
        -- Clean record_id: take first occurrence of duplicates
        record_id,
        
        -- Clean customer_name: remove nulls, trim spaces, title case
        initcap(trim(coalesce(customer_name, 'Unknown'))) as customer_name,
        
        -- Clean product_category: standardize case and trim, handle nulls
        case
            when lower(trim(coalesce(product_category, ''))) in ('электроника', 'elektronika') then 'Электроника'
            when lower(trim(coalesce(product_category, ''))) in ('одежда', 'odezhda') then 'Одежда'
            when lower(trim(coalesce(product_category, ''))) in ('продукты', 'produkty') then 'Продукты'
            when lower(trim(coalesce(product_category, ''))) in ('мебель', 'mebel') then 'Мебель'
            when lower(trim(coalesce(product_category, ''))) in ('книги', 'knigi') then 'Книги'
            else 'Прочее'
        end as product_category,
        
        -- Clean city: title case, remove nulls
        initcap(trim(coalesce(city, 'Unknown'))) as city,
        
        -- Clean status: standardize values
        case
            when lower(trim(coalesce(status, ''))) in ('активный', 'active') then 'Активный'
            when lower(trim(coalesce(status, ''))) in ('неактивный', 'inactive') then 'Неактивный'
            when lower(trim(coalesce(status, ''))) in ('приостановлен', 'suspended') then 'Приостановлен'
            else 'Неактивный'
        end as status,
        
        -- Clean payment_method: handle nulls
        coalesce(payment_method, 'Не указан') as payment_method,
        
        -- Clean amount: ensure positive, replace nulls with 0, cap at reasonable maximum
        case
            when amount is null then 0
            when amount < 0 then abs(amount)
            when amount > 1000000 then 1000000
            else amount
        end as amount,
        
        -- Clean quantity: ensure positive, replace nulls/negatives with 1
        case
            when quantity is null or quantity <= 0 then 1
            else quantity
        end as quantity,
        
        -- Clean discount_percent: ensure 0-100 range
        case
            when discount_percent is null then 0
            when discount_percent < 0 then 0
            when discount_percent > 100 then 100
            else discount_percent
        end as discount_percent,
        
        -- Clean transaction_date: handle nulls and future dates
        case
            when transaction_date is null then current_date
            when transaction_date > current_date then current_date
            else transaction_date
        end as transaction_date,
        
        -- Clean rating: ensure 1-5 range
        case
            when rating is null then 3.0
            when rating < 1 then 1.0
            when rating > 5 then 5.0
            else rating
        end as rating
        
    from (
        -- Deduplicate by taking the first occurrence based on ctid
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
            -- Filter by date range (after cleaning nulls and future dates)
            case
                when transaction_date is null then current_date
                when transaction_date > current_date then current_date
                else transaction_date
            end between start_date and end_date
        order by record_id, transaction_date, ctid
    ) as deduplicated;
    
    -- Get number of rows inserted
    get diagnostics rows_inserted = row_count;
    
    -- Log the operation
    raise notice 'ETL completed: % rows inserted into structured table for date range % to %', 
                 rows_inserted, start_date, end_date;
    
    return rows_inserted;
    
exception
    when others then
        raise exception 'ETL function failed: %', sqlerrm;
        return -1;
end;
$$;

comment on function s_psql_dds.fn_etl_data_load(date, date) is 
'ETL function to clean and transform data from unstructured to structured table for a given date range';
