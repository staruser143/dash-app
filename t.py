from pyspark.sql import functions as F
from pyspark.sql.types import StringType
from awsglue.context import GlueContext
from pyspark.context import SparkContext

# Initialize Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Custom class definition
class DataProcessor:
    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name
        self.df = None

    def load_data(self):
        # Load data from the database table into a DataFrame
        dyf = glueContext.create_dynamic_frame.from_catalog(
            database=self.database_name, 
            table_name=self.table_name
        )
        self.df = dyf.toDF()

    # Define the UDF as a static method or as a standalone function
    @staticmethod
    def example_udf(value):
        # Example UDF logic
        return value.upper() if value else None

    def process_data_with_udf(self):
        if self.df is None:
            raise ValueError("DataFrame is not loaded. Call load_data() first.")
        
        # Register the UDF
        to_upper_udf = F.udf(DataProcessor.example_udf, StringType())
        
        # Apply the UDF to the DataFrame
        processed_df = self.df.withColumn('new_column', to_upper_udf(self.df['column_name']))
        
        return processed_df

# Example usage
def main():
    # Initialize custom class with database and table names
    processor = DataProcessor(database_name="your_database", table_name="your_table")

    # Load data into DataFrame using the class method
    processor.load_data()

    # Process the DataFrame using a UDF
    processed_df = processor.process_data_with_udf()

    # Show the processed data
    processed_df.show()

if __name__ == "__main__":
    main()