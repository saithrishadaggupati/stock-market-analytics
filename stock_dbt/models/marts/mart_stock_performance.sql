with stock_prices as (
    select * from {{ ref('stg_fact_stock_prices') }}
),

stock_info as (
    select * from {{ ref('stg_dim_stock') }}
),

performance as (
    select
        s.ticker,
        s.sector,
        s.market,
        count(*)                                            as total_trading_days,
        round(avg(p.close), 2)                             as avg_close_price,
        round(min(p.close), 2)                             as min_close_price,
        round(max(p.close), 2)                             as max_close_price,
        round(avg(p.daily_pct_change), 4)                  as avg_daily_return,
        round(stddev(p.daily_pct_change) * sqrt(252), 4)   as annual_volatility,
        round(sum(p.volume), 0)                            as total_volume,
        round(avg(p.volume), 0)                            as avg_daily_volume
    from stock_prices p
    join stock_info s on p.ticker = s.ticker
    group by s.ticker, s.sector, s.market
)

select * from performance