with source as (
    select * from dim_stock
),

renamed as (
    select
        stock_id,
        ticker,
        sector,
        country,
        case
            when country = 'India' then 'Indian Market'
            else 'US Market'
        end as market
    from source
)

select * from renamed