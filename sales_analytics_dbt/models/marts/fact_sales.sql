SELECT

    order_id,
    customer_id,
    product,
    category,
    quantity,
    price,
    revenue,
    date

FROM {{ ref('stg_sales') }}