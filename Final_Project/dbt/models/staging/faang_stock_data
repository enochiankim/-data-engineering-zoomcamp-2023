{{ config(materialized='table') }}

select
    Date,
    Open,
    High,
    Low,
    Close,
    Adj_Close,
    Volume,
    file_name
from {{source('stock_data_table', 'faang_stock_data_partitioned')}}