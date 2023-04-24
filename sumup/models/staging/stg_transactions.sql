SELECT
    id as transaction_id,
    device_id,
    product_name,
    product_sku,
    category_name,
    amount,
    status,
    card_number,
    cvv,
    PARSE_DATETIME('%m/%d/%Y %T', created_at) as created_at,
    PARSE_DATETIME('%m/%d/%Y %T', happened_at) as happened_at

FROM `dbt-test-project-384521.raw_datasets.transactions_source`