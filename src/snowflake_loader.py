"""Snowflake loader module."""

import importlib
import os
from pathlib import Path
import pandas as pd

try:
    snowflake = importlib.import_module("snowflake.connector")
    # Import the highly optimized bulk-loading tool
    from snowflake.connector.pandas_tools import write_pandas 
except ImportError as exc:
    raise ImportError(
        "The snowflake-connector-python package is required to run this module."
    ) from exc


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    with env_path.open("r", encoding="utf-8") as env_file:
        for line in env_file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" not in stripped:
                continue

            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value:
                os.environ.setdefault(key, value)


def main():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_env_file(env_path)

    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    account = os.getenv("SNOWFLAKE_ACCOUNT")

    if not all([user, password, account]):
        raise RuntimeError(
            "Snowflake credentials are not set. Please add SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, and SNOWFLAKE_ACCOUNT to environment variables or .env."
        )

    print("Connecting to Snowflake...")
    # It is good practice to specify your database and schema right in the connection
    conn = snowflake.connect(
        user=user,
        password=password,
        account=account,
        database="SALES_DB", 
        schema="RAW"
    )

    try:
        print("Connected.")
        
        # 1. Load the Parquet data
        print("Reading Parquet data...")
        df = pd.read_parquet("data/processed_sales")
        print(f"Loaded {len(df)} rows from Parquet.")
        print(df.head())

        # 2. Convert column names to uppercase (Snowflake prefers uppercase identifiers)
        df.columns = [col.upper() for col in df.columns]

        # 3. Bulk insert using write_pandas
        print("Writing data to Snowflake...")
        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name="SALES_DATA",
            database="SALES_DB",
            schema="RAW",
            quote_identifiers=False # Set to True if your Snowflake table requires case-sensitive column names
        )

        if success:
            print(f"Success! {nrows} rows loaded into SALES_DATA.")
        else:
            print("Data load failed.")

    finally:
        # Use a finally block to ensure the connection closes even if an error occurs
        conn.close()
        print("Snowflake connection closed.")

if __name__ == "__main__":
    main()
    