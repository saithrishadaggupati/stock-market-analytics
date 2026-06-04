with stock_performance as (
    select * from {{ ref('mart_stock_performance') }}
),

sector_summary as (
    select
        sector,
        market,
        count(*)                                        as total_stocks,
        round(avg(avg_close_price), 2)                  as avg_price,
        round(avg(annual_volatility), 4)                as avg_volatility,
        round(avg(avg_daily_return), 4)                 as avg_daily_return,
        round(sum(total_volume), 0)                     as total_volume,
        min(ticker)                                     as least_volatile_stock
    from stock_performance
    group by sector, market
    order by avg_volatility asc
)

select * from sector_summary