# Real Time Retail Analytics with Spark and Kafka

This project focuses on analyzing real-time sales data for an e-commerce company, RetailCorp Inc., using Apache Spark Streaming and Kafka.

## Project Overview

The aim of this project is to read real-time sales data from a Kafka server, preprocess it, calculate various Key Performance Indicators (KPIs), and store these KPIs in JSON files for further analysis.

## Problem Statement

RetailCorp Inc. requires real-time computation of various KPIs using global sales data. The data includes invoice information from customer orders worldwide. An end-to-end data pipeline is typically built at the industry level to handle this task, utilizing tools like HDFS for data storage, real-time processing frameworks, and visualization tools like Tableau and PowerBI. The image below illustrates a complete data pipeline.

![data pipeline](https://github.com/user-attachments/assets/934e3e9c-453d-46ee-a195-902bf427fb3e)

In this project, we focus on the ‘Order Intelligence’ segment of this pipeline. The image below shows the architecture we will follow.

![project architecture](https://github.com/user-attachments/assets/5f09887e-205b-435a-9f19-72cf91b010c2)

## Tasks

1. Read sales data from a Kafka server.
2. Preprocess the data to derive additional columns like `total_cost`.
3. Calculate time-based KPIs and time- and country-based KPIs.
4. Store KPIs in HDFS for subsequent analysis.

## Data Dictionary

| Column         | Description                          |
|----------------|--------------------------------------|
| Invoice number | Unique identifier for the invoice    |
| Country        | Country where the order was placed   |
| Timestamp      | Time when the order was placed       |
| Type           | Indicates if it is a new or return order |
| SKU            | Stock Keeping Unit identifier for the product |
| Title          | Name of the product ordered          |
| Unit price     | Price per unit of the product        |
| Quantity       | Number of units ordered              |

## Features

- Real-time data processing with Spark Streaming.
- Kafka integration for data ingestion.
- Calculation of various KPIs based on time and country.
- Storage of KPIs in HDFS for further use.

## Prerequisites

- Apache Spark
- Apache Kafka
- Amazon EMR

## Getting Started

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/BharatPanera/spark-kafka-retail-analytics.git
    cd spark-kafka-retail-analytics
    ```

2. **Install Required Packages:**
    ```sh
    pip install kafka-python
    ```

3. **Run the Script:**
    ```sh
    export SPARK_KAFKA_VERSION=0.10
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 script.py
    ```
### Conclusion:
This project demonstrates how to use Apache Spark Streaming and Kafka to process real-time sales data, calculate important KPIs, and store the results in HDFS for further analysis. The solution is scalable and can handle large volumes of data, making it suitable for enterprise-level applications.
