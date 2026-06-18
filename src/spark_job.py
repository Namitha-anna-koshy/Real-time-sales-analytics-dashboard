from pyspark.sql import SparkSession
from pyspark.sql.functions import col


spark = SparkSession.builder \
    .appName("RealTimeSalesAnalyticsDashboard") \
    .getOrCreate()


df = spark.read.csv(
    "data/sales.csv",
    header=True,
    inferSchema=True
)


print("RAW DATA")
df.show()


print("SCHEMA")
df.printSchema()


clean_df = df.dropna()


clean_df = clean_df.withColumn(
    "revenue",
    col("quantity") * col("price")
)


print("PROCESSED DATA")
clean_df.show()


clean_df.write \
    .mode("overwrite") \
    .parquet(
        "data/processed_sales"
    )


print("Parquet created")


spark.stop()