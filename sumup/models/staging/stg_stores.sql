select
    id as store_id,
    name,
    address,
    city,
    country,
    PARSE_DATETIME('%m/%d/%Y %T', created_at) as created_at,    
    typology,
    customer_id

from {{ source('bigquery', 'stores_source') }}