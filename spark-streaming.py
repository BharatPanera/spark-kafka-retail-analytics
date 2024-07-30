import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Initialize Spark session  
spark = SparkSession \
    .builder \
    .appName("spark_streaming_retail") \
    .getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

# Read input from Kafka
ordersData = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "18.211.252.152:9092") \
    .option("failOnDataLoss", "false") \
    .option("startingOffsets", "earliest") \
    .option("subscribe", "real-time-project") \
    .load()

# Define the JSON schema for the data
schema = StructType([
    StructField("invoice_no", LongType(), False),
    StructField("country", StringType(), False),
    StructField("timestamp", TimestampType(), False),
    StructField("type", StringType(), False),
    StructField("items", ArrayType(StructType([
        StructField("SKU", StringType(), False),
        StructField("title", StringType(), False),
        StructField("unit_price", DoubleType(), False),
        StructField("quantity", IntegerType(), False)
    ])), True),
])

# Parse the JSON data
ordersDF = ordersData.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Define UDF functions
def calculate_total_price(items, type):
    total_price = 0
    for item in items:
        unit_price = item["unit_price"] if item["unit_price"] is not None else 0
        quantity = item["quantity"] if item["quantity"] is not None else 0
        total_price += unit_price * quantity

    return -total_price if type == "RETURN" else total_price

def calculate_total_items(items):
    total_items = 0
    for item in items:
        quantity = item["quantity"] if item["quantity"] is not None else 0
        total_items += quantity
    return total_items

def is_order(type):
    return 1 if type == "ORDER" else 0

def is_return(type):
    return 1 if type == "RETURN" else 0

# Register the UDFs
calculate_total_price_udf = udf(calculate_total_price, DoubleType())
calculate_total_items_udf = udf(calculate_total_items, IntegerType())
is_order_udf = udf(is_order, IntegerType())
is_return_udf = udf(is_return, IntegerType())

# Add the new fields to ordersDF
newOrdersDF = ordersDF \
    .withColumn("total_cost", calculate_total_price_udf(col("items"), col("type"))) \
    .withColumn("total_items", calculate_total_items_udf(col("items"))) \
    .withColumn("is_order", is_order_udf(col("type"))) \
    .withColumn("is_return", is_return_udf(col("type")))

# Write summarized input values to the console
queryOrders = newOrdersDF.select("invoice_no", "country", "timestamp", "total_cost", "total_items", "is_order", "is_return") \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime="1 minute") \
    .start()

# Calculate time-based KPIs - Orders Per Minute (OPM), Total volume of sales, and rate of returns
# Group by window
# Define a constant for the watermark duration
watermark_duration = "10 minutes"

AggByTime = newOrdersDF.withWatermark("timestamp", watermark_duration) \
    .groupBy(window(col("timestamp"), "1 minute")) \
    .agg(
        count("*").alias("OPM"),
        count(when(col("is_order") == 1, True)).alias("orders"),
        sum(col("total_cost")).alias("total_sale_volume"),
        count(when(col("is_return") == 1, True)).alias("returns")
    ) \
    .select(
        "window",
        "OPM",
        "total_sale_volume",
        (col("returns") / (col("orders") + col("returns"))).alias("rate_of_return"),
        (col("total_sale_volume") / (col("orders") + col("returns"))).alias("average_transaction_size")
    )

# Calculate time and country-based KPIs - Orders Per Minute (OPM), Total volume of sales, and rate of returns
# Group by country and window
AggByTimeAndCountry = newOrdersDF.withWatermark("timestamp", watermark_duration) \
    .groupBy(window(col("timestamp"), "1 minute"), col("country")) \
    .agg(
        count("*").alias("OPM"),
        count(when(col("is_order") == 1, True)).alias("orders"),
        sum(col("total_cost")).alias("total_sale_volume"),
        count(when(col("is_return") == 1, True)).alias("returns")
    ) \
    .select(
        "window",
        "country",
        "OPM",
        "total_sale_volume",
        (col("returns") / (col("orders") + col("returns"))).alias("rate_of_return")
    )

# Write the KPIs as JSON files to HDFS Location

# Write time-based KPIs to JSON files
queryKpiByTime = AggByTime.writeStream \
    .outputMode("append") \
    .format("json") \
    .option("path", "user/hadoop/real-time-project/kpis/time-based") \
    .option("checkpointLocation", "user/hadoop/real-time-project/kpis/time-based/checkpoint") \
    .trigger(processingTime="1 minute") \
    .start()

# Write time and country-based KPIs to JSON files
queryKpiByTimeAndCountry = AggByTimeAndCountry.writeStream \
    .outputMode("append") \
    .format("json") \
    .option("path", "user/hadoop/real-time-project/kpis/time-and-country-based") \
    .option("checkpointLocation", "user/hadoop/real-time-project/kpis/time-and-country-based/checkpoint") \
    .trigger(processingTime="1 minute") \
    .start()

# Terminate the Spark streaming job
queryOrders.awaitTermination()
queryKpiByTime.awaitTermination()
queryKpiByTimeAndCountry.awaitTermination()


