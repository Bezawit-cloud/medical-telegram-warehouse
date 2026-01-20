
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  -- tests/assert_no_future_messages.sql
select *
from "medical_telegram_db"."staging_marts"."fct_messages"
where date_key is not null
  and date_key >= 19000101
  and date_key <= 21001231
  and to_date(cast(date_key as text), 'YYYYMMDD') > current_date
  
  
      
    ) dbt_internal_test