--Transformed/silver data table which is focused on the store trancactions
with stores as (
    select 
        store_id 
    from {{ ref('stg_stores') }}
),
devices as (
    select
        device_id,
        type,
        store_id
    from {{ ref('stg_devices') }}
),
transactions as (
    select 
        transaction_id,
        device_id,
        product_sku,
        status,
        created_at,
        happened_at
    from {{ ref('stg_transactions') }}
)

SELECT *
FROM transactions t
LEFT JOIN devices USING(device_id)
LEFT JOIN stores USING(store_id)
ORDER BY transaction_id
