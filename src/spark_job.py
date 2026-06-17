from pyspark.sql import SparkSession
from pyspark.sql.functions import col


# Create Spark session
spark = SparkSession.builder \
    .appName("Real-time sales analytics dashboard") \
    .getOrCreate()


# Read raw data

df = spark.read.csv(
    "data/sales.csv",
    header=True,
    inferSchema=True
)
print("RAW DATA")
df.show()

print("SCHEMA")
df.printSchema()

# Data cleaning
clean_df = df.dropna()

# Add revenue column
clean_df = clean_df.withColumn(
    "revenue",
    col("quantity") * col("price")
)

print("PROCESSED DATA")
clean_df.show()



# Save as parquet
clean_df.write \
    .mode("overwrite") \
    .parquet(
        "data/processed_sales"
    )

print("Spark Pipeline Completed")
spark.stop()