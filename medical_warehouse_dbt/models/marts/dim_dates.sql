with dates as (

    select
        generate_series(
            min(message_date)::date,
            max(message_date)::date,
            interval '1 day'
        ) as date_day
    from {{ ref('stg_telegram_messages') }}

)

select
    date_day,
    extract(year from date_day)  as year,
    extract(month from date_day) as month,
    extract(day from date_day)   as day,
    extract(dow from date_day)   as day_of_week
from dates
