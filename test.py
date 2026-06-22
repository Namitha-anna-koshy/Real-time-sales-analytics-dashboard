import pandas as pd
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, coalesce

file_path = "data/processed_sales.csv"   # change filename

df = pd.read_csv(file_path)

print(df["date"].unique())
df = spark.read.parquet("data/processed_sales")

df.select("date").show(20)

df.printSchema()