Time travel in Apache Iceberg allows you to query data as it existed at a specific point in time or at a particular version or "snapshot" of the table. This feature is particularly useful for auditing, debugging, or reproducing analyses based on historical data. When using Iceberg tables on AWS with services like Amazon Athena, AWS Glue, or Spark on Amazon EMR, you can leverage time travel capabilities to access these past states.

How Time Travel Works in Iceberg

In Iceberg, every change to a table (inserts, updates, deletions) is stored as a new snapshot. Each snapshot is immutable and contains pointers to the data files that represent the state of the table at the time the snapshot was created. Iceberg’s metadata layer maintains a history of all snapshots, allowing you to query any past version without altering the underlying data.

Using Time Travel in AWS with Iceberg Tables

1. Querying by Snapshot ID

Each snapshot in Iceberg has a unique snapshot ID, which you can use to query the table's state at that particular version.

In Spark (AWS Glue or Amazon EMR):

# Spark SQL query to access data at a specific snapshot
spark.sql("""
    SELECT * FROM my_database.sales_data
    VERSION AS OF 123456789012345678
""")

In Athena:

Athena allows you to query Iceberg tables by specifying the snapshot ID in the SQL syntax:

SELECT * FROM my_database.sales_data FOR SYSTEM VERSION AS OF 123456789012345678;



2. Querying by Timestamp

You can also query data as it was at a specific timestamp. Iceberg will find the latest snapshot created at or before that timestamp.

In Spark (AWS Glue or Amazon EMR):

# Spark SQL query to access data as of a specific timestamp
spark.sql("""
    SELECT * FROM my_database.sales_data
    TIMESTAMP AS OF '2024-11-01 12:00:00'
""")

In Athena:

SELECT * FROM my_database.sales_data FOR SYSTEM TIME AS OF TIMESTAMP '2024-11-01 12:00:00';


How Time Travel Queries Work Internally

When you run a time-travel query:

1. Iceberg’s Metadata Layer: The query engine (e.g., Athena or Spark) accesses Iceberg’s metadata layer, which keeps track of all table snapshots and their associated metadata files.


2. Snapshot Resolution: Iceberg finds the snapshot that corresponds to the provided snapshot ID or timestamp.


3. Data Retrieval: The query engine reads only the data files referenced by the snapshot, reconstructing the table as it existed at that specific point in time.



Important Considerations

Retention Policies: By default, Iceberg retains snapshots indefinitely. However, you may want to set retention policies to periodically delete old snapshots and data files to reduce storage costs. This is done using the expire_snapshots procedure in Spark.

Query Performance: Querying older snapshots may be slightly slower if they reference many small files or if compaction hasn't been performed recently.

Permissions and Governance: When using Lake Formation with Iceberg, time travel queries will respect the same access controls, ensuring that users can only access snapshots they are authorized to view.


Example: Expiring Old Snapshots in Spark

To manage the storage space and retain only relevant snapshots, you can expire snapshots older than a specified timestamp:

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Expire Snapshots") \
    .getOrCreate()

# Expire snapshots older than a specified timestamp
spark.sql("""
    CALL my_database.system.expire_snapshots(
        table => 'sales_data',
        older_than => TIMESTAMP '2024-10-01 00:00:00'
    )
""")

Summary

Time travel with Iceberg on AWS enables you to flexibly query historical data using snapshot IDs or timestamps across Athena, Glue, and EMR. This powerful capability, combined with AWS data services, provides a reliable way to manage and explore your data history.

