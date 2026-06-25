from pyspark.sql import SparkSession
from pyspark.sql.functions import col, coalesce, expr


# Create Spark session
spark = SparkSession.builder \
    .appName("RealTimeSalesAnalyticsDashboard") \
    .getOrCreate()


# ---------------------------
# 1. READ RAW DATA
# ---------------------------

df = spark.read.csv(
    "data/sales.csv",
    header=True,
    inferSchema=True
)


print("RAW DATA")
df.show(10)


print("RAW SCHEMA")
df.printSchema()


# ---------------------------
# 2. DATA CLEANING
# ---------------------------

# Remove rows with null values
clean_df = df.dropna()


# ---------------------------
# 3. CREATE REVENUE COLUMN
# ---------------------------

clean_df = clean_df.withColumn(
    "revenue",
    col("quantity") * col("price")
)


# ---------------------------
# 4. STANDARDIZE DATE COLUMN
# ---------------------------

# Handles both:
# 2025-11-28
# 03/01/2025

clean_df = clean_df.withColumn(
    "date",
    coalesce(
        expr("try_to_date(date, 'yyyy-MM-dd')"),
        expr("try_to_date(date, 'MM/dd/yyyy')")
    )
)


# ---------------------------
# 5. FINAL CHECK
# ---------------------------

print("PROCESSED DATA")

clean_df.show(20, False)


print("FINAL SCHEMA")

clean_df.printSchema()


# ---------------------------
# 6. WRITE PROCESSED DATA
# ---------------------------

clean_df.write \
    .mode("overwrite") \
    .parquet(
        "data/processed_sales"
    )


print("Parquet created successfully")


spark.stop()