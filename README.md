# Real-Time Retail Analytics with Spark and Kafka

This project focuses on real-time sales data analysis for an e-commerce company, RetailCorp Inc., using Apache Spark Streaming and Kafka.

## Project Overview

The project reads real-time sales data from a Kafka server, preprocesses the data, calculates various Key Performance Indicators (KPIs), and stores the KPIs in JSON files for further analysis.

## Architecture

[Include architecture image]

## Features

- Real-time data processing using Spark Streaming
- Integration with Kafka for data ingestion
- Calculation of time-based and country-based KPIs
- Storing KPIs in JSON files for further analysis

## Prerequisites

- Apache Spark
- Apache Kafka

## Getting Started

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/spark-kafka-retail-analytics.git
    cd spark-kafka-retail-analytics
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure Kafka and Spark settings in `configs/`.

4. Run the script:
    ```sh
    export SPARK_KAFKA_VERSION=0.10
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 script.py
    ```

## Data Dictionary

| Column          | Description                            |
|-----------------|----------------------------------------|
| Invoice number  | Identifier of the invoice              |
| Country         | Country where the order is placed      |
| Timestamp       | Time at which the order is placed      |
| Type            | Whether this is a new order or a return order |
| SKU             | Identifier of the product being ordered |
| Title           | Name of the product ordered            |
| Unit price      | Price of a single unit of the product  |
| Quantity        | Quantity of the product being ordered  |
