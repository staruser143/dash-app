To run the PySpark script as an AWS Glue job and view the DataFrame output in AWS CloudWatch logs, you'll need to make a few changes to the script:

1. Import AWS Glue Libraries

AWS Glue requires the glueContext and related libraries instead of directly using SparkSession:

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
import sys
from pyspark.context import SparkContext

2. Initialize GlueContext and Job

Replace the initialization of SparkSession with GlueContext:

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

3. Modify the Class to Use GlueContext

Ensure that the class uses the spark session from the GlueContext:

class DataFrameEnhancer:
    def __init__(self, glueContext):
        self.spark = glueContext.spark_session

    # Rest of the class remains the same...

4. Print DataFrame to CloudWatch Logs

To view the DataFrame output in AWS CloudWatch logs, use the show() method with truncate=False and print() for small outputs. Note that printing large DataFrames may overwhelm the logs, so it's usually better to show only the top N rows:

if __name__ == "__main__":
    # Initialize Glue job and context
    args = getResolvedOptions(sys.argv, ['JOB_NAME'])
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session

    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)

    # Example DataFrame
    data = [("a|b|c",), ("d|e|f",), ("g|h|i",)]
    df = spark.createDataFrame(data, ["original_field"])

    enhancer = DataFrameEnhancer(glueContext)
    enhanced_df = enhancer.add_dynamic_fields(df, "original_field")
    
    # Show the DataFrame in logs
    enhanced_df.show(truncate=False)

    # End the Glue job
    job.commit()

5. Deploy and Run as AWS Glue Job

Deploy: Upload the script to an S3 bucket.

Create AWS Glue Job: In the AWS Glue console, create a new Glue job. Specify the script location in S3, set the IAM role, and configure other settings as needed.

Run the Job: Execute the Glue job. AWS Glue will automatically stream logs to AWS CloudWatch.


6. View Logs in AWS CloudWatch

1. Access CloudWatch: Go to the AWS Management Console, and navigate to CloudWatch.


2. Locate Logs: Find the log group associated with your Glue job. The log stream will contain logs from the job, including the output of enhanced_df.show().



Additional Considerations

Job Bookmarks: If your Glue job runs incrementally on a dataset, consider enabling job bookmarks.

IAM Roles: Ensure that the IAM role associated with the Glue job has appropriate permissions for accessing S3, Glue resources, and CloudWatch Logs.


This setup will allow your PySpark script to run on AWS Glue, and you can view the DataFrame's output in CloudWatch logs.

