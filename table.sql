-- Athena SQL to create an Iceberg table with a specified S3 location
CREATE TABLE my_database.sales_data (
    id BIGINT,
    name STRING,
    amount DOUBLE,
    sale_date DATE
)
PARTITIONED BY (sale_date)
LOCATION 's3://mybucket/myfolder/sales_data'
TBLPROPERTIES (
    'table_type' = 'ICEBERG'
);