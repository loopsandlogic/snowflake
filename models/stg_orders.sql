{{
    config(
        materialized='incremental'
    )
}}

select
    id as order_id,
    user_id as customer_id,
    order_date,
    status

from {{ source('jaffle_shop', 'orders') }}
{% if is_incremental() %}
    -- this filter will only be applied on an incremental run
    where order_date > (select max(order_date) from {{ this }}) 
{% endif %}