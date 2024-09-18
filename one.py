from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Initialize Spark session (Assuming this is not in AWS Glue context)
spark = SparkSession.builder.appName("SampleDataFrame").getOrCreate()

# Custom class definition
class DataProcessor:
    def __init__(self, df: DataFrame):
        # Initialize with a DataFrame directly
        self.df = df

    def process_data(self):
        if self.df is None:
            raise ValueError("DataFrame is not initialized.")
        
        # Perform some processing on the DataFrame (example: filtering)
        processed_df = self.df.filter(self.df['age'] > 25)
        return processed_df

def create_sample_dataframe(spark: SparkSession) -> DataFrame:
    # Create a sample DataFrame with some mock data
    sample_data = [
        ("Alice", 30),
        ("Bob", 20),
        ("Charlie", 40)
    ]
    
    # Define the schema for the DataFrame
    schema = StructType([
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True)
    ])
    
    # Create DataFrame
    df = spark.createDataFrame(sample_data, schema)
    return df

def main():
    # Create a sample DataFrame
    sample_df = create_sample_dataframe(spark)
    
    # Initialize the DataProcessor class with the sample DataFrame
    processor = DataProcessor(sample_df)
    
    # Process the DataFrame
    processed_df = processor.process_data()
    
    # Show the processed data
    processed_df.show()

if __name__ == "__main__":
    main()