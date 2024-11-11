When a table is created in Iceberg using either Athena or Spark, the data for that table is stored in the following structured manner in Amazon S3 (or other cloud storage):

1. Data Files:

Data is stored in columnar formats like Parquet or ORC, which Iceberg supports by default for efficiency and performance in analytical queries.

Files are organized by partitions (if any) defined for the table, with each data file containing a subset of rows based on those partition criteria. For example, a table partitioned by date may store files under a folder structure like s3://mybucket/table_name/date=2024-10-28/.



2. Metadata Files:

Iceberg uses a metadata layer to track table schema, partitions, data files, and snapshots, allowing it to offer features like time travel and schema evolution.

This metadata is stored as JSON files in the metadata folder within the table’s directory. Key metadata files include:

Manifest Lists: These contain information about each manifest file (essentially a list of all data files for a snapshot).

Manifests: These list specific data files included in a snapshot, with pointers to each file's path, row count, and statistics.

Snapshot Files: These files track changes to the table, allowing you to roll back to previous versions or use time travel features.




3. Snapshot Management:

Iceberg uses snapshots to manage data versions. Each time new data is added or existing data is modified, a new snapshot is created, pointing to new manifest lists and manifests. This way, previous data versions are preserved, supporting time travel.




Example Directory Structure

Suppose you create a table named sales_data. The S3 structure might look like this:

s3://mybucket/sales_data/
|-- data/                                # Contains Parquet or ORC data files
|    |-- date=2024-10-28/
|         |-- part-00001.parquet
|         |-- part-00002.parquet
|
|-- metadata/                            # Contains metadata files for table management
|    |-- v1.metadata.json
|    |-- v2.metadata.json
|    |-- snapshot-00001.json
|    |-- snapshot-00002.json

This structure allows Iceberg to manage the data efficiently, making it easier to query and support advanced features like time travel and schema evolution without affecting the underlying data files directly.

