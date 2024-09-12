Yes, you can add log messages to your PySpark script to make them visible in AWS CloudWatch logs. Logging in PySpark, when running under AWS Glue, can be done using Python's logging module or by simply using print statements.

1. Using Python's logging Module

Here's how to set up logging and integrate it into your PySpark script:

a. Import and Configure Logging

import logging
import sys

# Configure logging
logging.basicConfig(
    stream=sys.stdout,  # Redirect logs to stdout so Glue can capture them
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s %(levelname)s %(message)s'  # Format of the log messages
)
logger = logging.getLogger()

b. Add Log Messages

You can now add log messages at different points in your script:

class DataFrameEnhancer:
    def __init__(self, glueContext):
        self.spark = glueContext.spark_session
        logger.info("Initialized DataFrameEnhancer with GlueContext.")

    def parse_field(self, value):
        fields = value.split('|')
        logger.debug(f"Parsed fields: {fields}")
        return fields

    def register_udf(self):
        logger.info("Registering UDF.")
        return udf(self.parse_field, ArrayType(StringType()))

    def add_dynamic_fields(self, df, field_name):
        logger.info(f"Adding dynamic fields based on {field_name}.")
        parse_field_udf = self.register_udf()
        df = df.withColumn("parsed_fields", parse_field_udf(df[field_name]))
        df = df.withColumn("field1", df["parsed_fields"].getItem(0)) \
               .withColumn("field2", df["parsed_fields"].getItem(1)) \
               .withColumn("field3", df["parsed_fields"].getItem(2))
        df = df.drop("parsed_fields")
        logger.info("Dynamic fields added successfully.")
        return df

if __name__ == "__main__":
    # Initialize Glue job and context
    args = getResolvedOptions(sys.argv, ['JOB_NAME'])
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session

    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)
    logger.info("Glue job initialized.")

    # Example DataFrame
    data = [("a|b|c",), ("d|e|f",), ("g|h|i",)]
    df = spark.createDataFrame(data, ["original_field"])
    logger.info("Sample DataFrame created.")

    enhancer = DataFrameEnhancer(glueContext)
    enhanced_df = enhancer.add_dynamic_fields(df, "original_field")
    
    # Show the DataFrame in logs
    enhanced_df.show(truncate=False)
    logger.info("DataFrame content displayed in logs.")

    # End the Glue job
    job.commit()
    logger.info("Glue job completed successfully.")

2. Using print Statements

If you prefer simplicity or don't need advanced logging features, you can use print statements to log messages:

print("Initialized DataFrameEnhancer with GlueContext.")
print("Adding dynamic fields based on field_name.")
print("Dynamic fields added successfully.")
print("Sample DataFrame created.")
print("DataFrame content displayed in logs.")
print("Glue job completed successfully.")

3. Viewing Logs in AWS CloudWatch

Regardless of whether you use logging or print, the logs will be available in AWS CloudWatch under the log group associated with your Glue job. You can access them via the AWS Management Console:

1. Go to CloudWatch: Navigate to the CloudWatch service.


2. Log Groups: Find the log group corresponding to your Glue job.


3. Log Streams: Inside the log group, locate the appropriate log stream to view the logs.



Summary

Logging with logging Module: Provides more control over the log format and log levels (e.g., INFO, DEBUG, ERROR).

Simple print Statements: Quick and easy for straightforward logging without additional setup.


Both approaches will ensure that your log messages are visible in AWS CloudWatch logs when running your AWS Glue job.

