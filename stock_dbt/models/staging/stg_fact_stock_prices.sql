with source as (
    select * from fact_stock_prices
),

renamed as (
    select
        fact_id,
        date,
        ticker,
        sector,
        country,
        open,
        high,
        low,
        close,
        volume,
        round(close - open, 4)                      as daily_price_change,
        round((close - open) / open * 100, 4)        as daily_pct_change,
        round(high - low, 4)                         as daily_range
    from source
)

select * from renamed