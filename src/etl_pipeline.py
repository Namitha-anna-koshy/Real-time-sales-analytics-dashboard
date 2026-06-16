import pandas as pd

# Extract
df = pd.read_csv("../data/sales.csv")
print("Raw data(first 10 rows only) :")
print(df.head(10))
# Transform

df["revenue"] = df["quantity"] * df["price"] # create revenue column
df = df.dropna() # remove missing values
print("Cleaned data(first 10 rows only :)")
print(df.head(10))

# Load
df.to_csv(
    "../data/processed_sales.csv",
    index=False
)
print("\nPipeline Completed!")