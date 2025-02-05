# Import necessary libraries
import sys
import json
import boto3
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, current_timestamp, expr
)
from pyspark.sql.types import DecimalType
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions

# ==============================
#  INITIALIZE SPARK & GLUE CONTEXT
# ==============================

# Create a Spark session with optimized configurations for Glue and Hudi
spark = SparkSession.builder \
    .appName("Glue-Hudi-Crypto-ETL") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.hive.convertMetastoreParquet", "false") \
    .getOrCreate()

# Initialize Glue context to work with AWS Glue Dynamic Frames
glueContext = GlueContext(spark)

# Set Spark SQL configurations for legacy time parsing
spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")

# ==============================
#  CONFIGURATION VARIABLES
# ==============================

# Define source and destination database & table names
SOURCE_DATABASE = "crypto"
SOURCE_TABLE = "crypto_table_crypto_data_project_nrt"

HUDI_DATABASE = "crypto"
HUDI_TABLE = "processed_crypto_txn"
HUDI_PATH = "s3://crypto-post-processing-nrt/crypto_processed/"

# ==============================
#  READ DATA FROM GLUE CATALOG
# ==============================

# Read incremental data from AWS Glue Data Catalog
firehose_df = glueContext.create_dynamic_frame.from_catalog(
    database=SOURCE_DATABASE, table_name=SOURCE_TABLE
).toDF()

# ==============================
#  DATA TRANSFORMATION
# ==============================

# Convert columns to appropriate data types for consistency
firehose_df = firehose_df \
    .withColumn("quantity", col("quantity").cast(DecimalType(10, 6))) \
    .withColumn("price", col("price").cast(DecimalType(10, 2))) \
    .withColumn("trade_fee", col("trade_fee").cast(DecimalType(10, 4))) \
    .withColumn("ingestion_time", current_timestamp())

# ==============================
#  RISK FLAGGING (High-Risk Trades)
# ==============================

# Classify transactions based on trade value
firehose_df = firehose_df.withColumn(
    "risk_flag",
    when(col("quantity") * col("price") > 500000, "HIGH_RISK")
    .when(col("quantity") * col("price") > 100000, "MEDIUM_RISK")
    .otherwise("LOW_RISK")
)

# ==============================
#  PRICE NORMALIZATION ACROSS EXCHANGES
# ==============================

# Define price adjustment factors per exchange
exchange_price_multiplier = {
    "Binance": 1.00,
    "Coinbase": 1.02,
    "Kraken": 0.98,
    "OKX": 1.01,  
    "FTX": 0.99,
    "Bitfinex": 1.03
}

# Apply exchange-specific price normalization
exchange_case_expr = "CASE " + " ".join([
    f"WHEN exchange = '{exch}' THEN price * {factor}" for exch, factor in exchange_price_multiplier.items()
]) + " ELSE price END"

firehose_df = firehose_df.withColumn("normalized_price", expr(exchange_case_expr).cast(DecimalType(10, 2)))

# ==============================
#  TRADE FEE ADJUSTMENT BASED ON TRANSACTION SIZE
# ==============================

firehose_df = firehose_df.withColumn(
    "adjusted_trade_fee",
    when(col("quantity") * col("price") >= 100000, col("trade_fee") * 0.9)  # 10% discount for high-value trades
    .when(col("quantity") * col("price") >= 50000, col("trade_fee") * 0.95)  # 5% discount for mid-range trades
    .otherwise(col("trade_fee"))  # No discount for small trades
)

# ==============================
#  USER CATEGORIZATION (Based on Trade Volume)
# ==============================

firehose_df = firehose_df.withColumn(
    "user_category",
    when(col("quantity") > 2, "VIP Trader")  # Large traders
    .when(col("quantity") > 1, "Active Trader")  # Frequent traders
    .otherwise("Casual Trader")  # Small-scale traders
)

# ==============================
#  TIME BUCKET CREATION (For Market Analysis)
# ==============================

# Group trades by hourly time buckets
firehose_df = firehose_df.withColumn(
    "hour_bucket",
    expr("date_format(timestamp, 'yyyy-MM-dd HH:00:00')")
)

# ==============================
#  FILTERING INVALID OR FAILED TRADES
# ==============================

firehose_df = firehose_df.filter(
    (col("trade_status") != "FAILED") &  # Remove failed trades
    (col("quantity") > 0) &  # Ensure positive trade volume
    (col("price") > 0)  # Ensure valid pricing
)

# ==============================
#  WRITE PROCESSED DATA TO HUDI TABLE
# ==============================

# Define Hudi configurations for upsert operation
hudi_options = {
    "hoodie.table.name": HUDI_TABLE,
    "hoodie.datasource.write.storage.type": "COPY_ON_WRITE",
    "hoodie.datasource.write.recordkey.field": "transaction_id",
    "hoodie.datasource.write.partitionpath.field": "exchange",
    "hoodie.datasource.write.precombine.field": "timestamp",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.datasource.hive_sync.enable": "true",
    "hoodie.datasource.hive_sync.database": HUDI_DATABASE,
    "hoodie.datasource.hive_sync.table": HUDI_TABLE,
    "hoodie.datasource.hive_sync.partition_fields": "exchange",
    "hoodie.datasource.hive_sync.mode": "hms",
    "path": HUDI_PATH
}

# ==============================
#  ENSURE DATABASE EXISTS
# ==============================

# Create Hudi database if it does not exist
spark.sql(f"CREATE DATABASE IF NOT EXISTS {HUDI_DATABASE}")

# ==============================
#  PERFORM HUDI MERGE (Upsert)
# ==============================

# Write processed data to Hudi table
firehose_df.write.format("hudi").options(**hudi_options).mode("append").save()

print("Hudi Upsert Completed Successfully !!")