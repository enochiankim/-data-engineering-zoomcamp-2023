{{ config(materialized='table') }}


with 
stock_data_main as (
    select Date,
    Open,
    High,
    Low,
    Close,
    Adj_Close,
    Volume,
    file_name 
    from {{ref("faang_stock_data")}}),
    
    stock_data_symbol as (
        select 
        Company,
        Stock_Symbol 
        from {{ref("faang_stock_symbol")}})

select 
s.company as Company,
s.Stock_Symbol as Ticker_Symbol,
Date,
Open,
High, 
Low,
Close,
Adj_Close,
Volume
from stock_data_main m join stock_data_symbol s on m.file_name = s.company