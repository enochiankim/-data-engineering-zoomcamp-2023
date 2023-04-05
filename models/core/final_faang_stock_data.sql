{{ config(materialized='table') }}


with faang_stock_data_main(select * from {{ref("faang_stock_data")}})