
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select *
from "medical_telegram_db"."staging_marts"."fct_messages"
where view_count < 0
  
  
      
    ) dbt_internal_test