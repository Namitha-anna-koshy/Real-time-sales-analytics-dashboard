WITH sales_data AS (
    SELECT

        *,
        ROW_NUMBER() OVER (
            ORDER BY order_id
        ) AS row_id

    FROM SALES_DB.RAW.SALES_DATA

)

SELECT
    MD5(
        CONCAT(
            order_id,
            customer_id,
            product,
            row_id
        )
    ) AS sales_id,

    order_id,
    customer_id,
    product,
    category,
    quantity,
    price,
    revenue,
    date

FROM sales_data