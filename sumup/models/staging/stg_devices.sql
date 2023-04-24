SELECT
    id as device_id,
    type,
    store_id

FROM {{ source('bigquery', 'devices_source') }}