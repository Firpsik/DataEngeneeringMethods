-- Функция перекладки данных из staging в целевую таблицу MySQL
delimiter //

create procedure if not exists s_sql_dm.fn_dm_data_stg_to_dm_load(
    in start_dt date,
    in end_dt date
)
begin
    declare rows_affected int default 0;
    
    -- Начало транзакции
    start transaction;
    
    -- Удаление данных за период из целевой таблицы
    delete from s_sql_dm.t_dm_task
    where transaction_date between start_dt and end_dt;
    
    -- Вставка данных из staging
    insert into s_sql_dm.t_dm_task (
        record_id,
        customer_id,
        customer_name,
        product_category_id,
        product_category,
        city_id,
        city,
        status_id,
        status,
        payment_method_id,
        payment_method,
        amount,
        quantity,
        discount_percent,
        transaction_date,
        rating
    )
    select
        record_id,
        customer_id,
        customer_name,
        product_category_id,
        product_category,
        city_id,
        city,
        status_id,
        status,
        payment_method_id,
        payment_method,
        amount,
        quantity,
        discount_percent,
        transaction_date,
        rating
    from s_sql_dm.t_dm_stg_task
    where transaction_date between start_dt and end_dt;
    
    set rows_affected = row_count();
    
    -- Коммит транзакции
    commit;
    
    select concat('MySQL DM load completed: ', rows_affected, ' rows loaded for period ', 
                  start_dt, ' to ', end_dt) as result;
    
end //

delimiter ;
