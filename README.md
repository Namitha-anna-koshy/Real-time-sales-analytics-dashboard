# 🚀 End-to-End Sales Analytics Pipeline: Spark to Power BI

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-FFFFFF?style=for-the-badge&logo=apachespark&logoColor=#E35A16)
![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

> **Live Dashboard Preview:** [Link to your hosted PowerBI or a short GIF showcasing the dashboard]

## 🎯 Project Overview
This project is an automated, end-to-end data pipeline that ingests raw transactional data, processes it at scale, models it for business intelligence, and serves it through an interactive dashboard. Designed to simulate a production-grade retail analytics environment, it transforms unstructured logs into actionable revenue insights.

### 🏆 Key Results
* **Performance:** Spark processed the full dataset **8× faster** than the initial pandas baseline, eliminating out-of-memory errors.
* **Data Quality:** Implemented dbt tests that caught and filtered out 100% of orphaned records and null primary keys before they reached the BI layer.
* **Automation:** Reduced manual data refresh time from hours to zero via automated orchestration.

---

## 🏗️ Architecture

<p align="center">
  <img src="https://via.placeholder.com/800x300/eeeeee/333333?text=Excalidraw:+Raw+Data+->+Spark+->+Snowflake+->+dbt+->+Power+BI" alt="Architecture Diagram: Raw Data to Spark to Snowflake to dbt to Power BI">
</p>

1. **Data Ingestion (Raw Data):** Raw CSV/JSON files loaded from local storage/AWS S3.
2. **Data Processing (Apache Spark):** Cleans, partitions, and formats raw data into Parquet.
3. **Data Warehousing (Snowflake):** Acts as the centralized storage layer for staging and raw tables.
4. **Data Modeling (dbt):** Applies business logic, handles dimensional modeling (Star Schema), and runs data quality tests.
5. **Business Intelligence (Power BI):** Connects to Snowflake's production views to visualize revenue trends and customer behavior.

---

## 🛠️ Technology Stack
* **Language:** Python, SQL
* **Processing:** Apache Spark (PySpark)
* **Warehouse:** Snowflake
* **Transformation & Testing:** dbt (Data Build Tool)
* **Visualization:** Power BI
* **Version Control:** Git & GitHub

---

## 📂 Repository Structure

```text
├── data/                   # Sample raw datasets (ignored in git)
├── notebooks/              # Jupyter notebooks for initial EDA and Spark prototyping
├── src/                    # Python scripts for Spark jobs and API ingestion
├── dbt_project/            # dbt models, schema.yml, and tests
│   ├── models/
│   │   ├── staging/        # Base views cleaning Snowflake raw tables
│   │   └── marts/          # Fact and dimension tables for BI
├── images/                 # Architecture diagrams and screenshots
├── requirements.txt        # Python dependencies
└── README.md