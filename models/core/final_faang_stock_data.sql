{{ config(materialized='table') }}


with 
stock_data_main as (select * from {{ref("faang_stock_data")}}),
stock_data_symbol as (select * from {{ref("faang_stock_symbol")}})

select 
Stock_Symbol,
Company,
Date,
Open,
High, 
Low,
Close
Adj_Close,
Volume
from stock_data_main m join stock_data_symbol s on m.file_name = s.company