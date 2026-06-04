\# Data Dictionary



This document describes every table and column in the stock market analytics pipeline — from raw ingestion through dbt staging models to the final mart layer.



\---



\## Source Tables (DuckDB)



\### `dim\_stock`



Dimension table holding one row per stock with static attributes.



| Column | Type | Description |

|---|---|---|

| stock\_id | INTEGER | Primary key |

| ticker | TEXT | Stock ticker symbol (e.g. AAPL, RELIANCE.NS) |

| sector | TEXT | Industry sector (e.g. Technology, Energy) |

| country | TEXT | Country of listing — India or US |



\---



\### `fact\_stock\_prices`



Fact table with one row per stock per trading day.



| Column | Type | Description |

|---|---|---|

| fact\_id | INTEGER | Primary key |

| date | DATE | Trading date |

| ticker | TEXT | Foreign key to dim\_stock |

| sector | TEXT | Sector at time of record |

| country | TEXT | Country at time of record |

| open | FLOAT | Opening price |

| high | FLOAT | Intraday high |

| low | FLOAT | Intraday low |

| close | FLOAT | Closing price |

| volume | INTEGER | Shares traded |



\---



\## Staging Models (dbt)



\### `stg\_dim\_stock`



Cleans and enriches `dim\_stock`. Adds a `market` label derived from the `country` column.



| Column | Type | Description |

|---|---|---|

| stock\_id | INTEGER | Passed through from source |

| ticker | TEXT | Passed through from source |

| sector | TEXT | Passed through from source |

| country | TEXT | Passed through from source |

| market | TEXT | Derived — "Indian Market" if country = India, else "US Market" |



\---



\### `stg\_fact\_stock\_prices`



Cleans `fact\_stock\_prices` and computes three derived price metrics.



| Column | Type | Description |

|---|---|---|

| fact\_id | INTEGER | Passed through from source |

| date | DATE | Passed through from source |

| ticker | TEXT | Passed through from source |

| sector | TEXT | Passed through from source |

| country | TEXT | Passed through from source |

| open | FLOAT | Passed through from source |

| high | FLOAT | Passed through from source |

| low | FLOAT | Passed through from source |

| close | FLOAT | Passed through from source |

| volume | INTEGER | Passed through from source |

| daily\_price\_change | FLOAT | close − open, rounded to 4 dp |

| daily\_pct\_change | FLOAT | (close − open) / open × 100, rounded to 4 dp |

| daily\_range | FLOAT | high − low, rounded to 4 dp |



\---



\## Mart Models (dbt)



\### `mart\_stock\_performance`



One row per ticker. Aggregates daily price history into per-stock performance metrics. Joins staging fact and dimension models.



| Column | Type | Description |

|---|---|---|

| ticker | TEXT | Stock ticker |

| sector | TEXT | Industry sector |

| market | TEXT | Indian Market or US Market |

| total\_trading\_days | INTEGER | Number of trading days in the dataset |

| avg\_close\_price | FLOAT | Mean closing price across all days |

| min\_close\_price | FLOAT | Lowest closing price recorded |

| max\_close\_price | FLOAT | Highest closing price recorded |

| avg\_daily\_return | FLOAT | Mean of daily\_pct\_change |

| annual\_volatility | FLOAT | Annualised volatility — stddev(daily\_pct\_change) × √252 |

| total\_volume | INTEGER | Sum of all daily volumes |

| avg\_daily\_volume | INTEGER | Mean daily trading volume |



\---



\### `mart\_sector\_summary`



One row per sector + market combination. Rolls up `mart\_stock\_performance` into sector-level aggregates.



| Column | Type | Description |

|---|---|---|

| sector | TEXT | Industry sector |

| market | TEXT | Indian Market or US Market |

| total\_stocks | INTEGER | Number of tickers in this sector/market group |

| avg\_price | FLOAT | Mean of avg\_close\_price across tickers |

| avg\_volatility | FLOAT | Mean of annual\_volatility across tickers |

| avg\_daily\_return | FLOAT | Mean of avg\_daily\_return across tickers |

| total\_volume | INTEGER | Sum of total\_volume across tickers |

| least\_volatile\_stock | TEXT | Ticker with the lowest volatility (min alphabetically when tied) |



\---



\## Derived Metric Notes



\- \*\*annual\_volatility\*\* uses the standard 252 trading days per year convention

\- \*\*daily\_pct\_change\*\* can be negative — indicates a down day

\- \*\*market\*\* is a derived convenience column, not stored in the raw source

