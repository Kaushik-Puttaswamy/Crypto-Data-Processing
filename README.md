# Crypto Data Processing and Analysis Pipeline Using AWS Glue, Kinesis, DynamoDB, Athena and QuickSight

## 📌 Project Overview

The Crypto Data Processing Pipeline is an end-to-end data processing solution designed to handle cryptocurrency transactions in real time. It leverages AWS Glue, AWS Lambda, Kinesis Firehose, DynamoDB Streams, and Hudi for efficient ETL and analytics. The project processes raw transaction data, performs transformations, categorizes trades based on risk, and stores processed data in an S3-based Hudi table for further analysis uisng AWS QucikSight.

• Real-time data ingestion from DynamoDB streams

• CDC (Change Data Capture) processing with Kinesis Firehose

• Spark-based ETL with AWS Glue and Apache Hudi

• Data lake storage with S3 and AWS Glue Catalog

• Interactive analytics with Athena and QuickSight

## 📂 Project Structure

Crypto-Data-Processing/

│── crypto_nrt_etl_glue_job.py               # AWS Glue ETL script for data transformation & storage

│── lambda_transformer.py                     # AWS Lambda function for processing DynamoDB Streams

│── mock_crypto_data_to_dynamodb.py           # Script to simulate crypto transactions and insert them into DynamoDB

│── Project Execution Screenshots/            # Folder containing setup and execution screenshots

│── Project architecture                      # High-level architecture and data flow

└── README.md                                 # Project documentation (this file)

## ✨ Key Features

• Real-Time Risk Analysis: Flag high-value trades (>$500k)

• Multi-Exchange Normalization: Price adjustments per exchange

• Dynamic Fee Calculation: Volume-based fee discounts

• Time-Bucket Aggregation: Hourly trade analysis

• ACID Compliance: Apache Hudi for UPSERT operations

## 🛠 Prerequisites

Before setting up the Crypto Data Processing and Analysis Pipeline, ensure you have the following:

1. AWS Account & Services
	
 • An AWS Account with access to:
	
 • AWS Glue (for ETL and data transformation)
	
 • AWS DynamoDB (for storing raw crypto transactions)
	
 • AWS Kinesis Firehose (for real-time streaming)
	
 • AWS Lambda (for data transformation)
	
 • AWS S3 (for storing raw and processed data)
	
 • AWS Athena (for querying processed data)
	
 • AWS QuickSight (for visualizing insights)

2. AWS CLI & SDKs
	
 • Install and configure AWS CLI:

```pip install awscli```

```aws configure``` 

3. Python & Dependencies
	
• Install Python 3.x and required libraries:

```pip install faker``` 

```pip install boto3``` 

4. Permissions & IAM Roles

• Create IAM roles with the following policies:

• Glue Service Role (AWSGlueServiceRole)

• Lambda Execution Role (AWSLambdaBasicExecutionRole)

• Kinesis Firehose Access Policy

• DynamoDB Stream Access Policy

5. AWS S3 Bucket for Storage
	
• Create an S3 bucket for storing raw and processed data.

6. Enable DynamoDB Streams

• Enable DynamoDB Streams on the CryptoTransactions table for real-time data ingestion.

## 🏛 Project Architecture


This project follows a real-time data ingestion and processing pipeline:
	
 1.	Data Generation (Mock Transactions)
	•	A Python script (mock_crypto_data_to_dynamodb.py) continuously generates mock crypto transactions.
	•	The data is inserted into AWS DynamoDB.

2.	Data Streaming & Transformation
	•	DynamoDB Streams captures changes and forwards them to AWS Kinesis Firehose.
	•	A Lambda function (lambda_transformer.py) transforms the data from DynamoDB’s format to JSON.
	
 3.	Real-Time ETL Processing (AWS Glue)
	•	AWS Glue reads data from S3 (landing zone).
	•	Performs data transformations, including:
	•	Risk flagging based on trade value.
	•	Price normalization across exchanges.
	•	Fee adjustments based on transaction size.
	•	User categorization based on trade volume.
	•	Writes processed data into an AWS S3-based Hudi table.
	
 4.	Data Storage & Analytics
	•	Processed Data: Stored in an S3 Hudi table (processed_crypto_txn).
	•	Querying: AWS Athena is used to query Hudi tables.
	•	Visualization: QuickSight dashboards are built on Athena queries.























https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/78dd677e-34d1-4a4f-9b78-82a2f97863ba/views/fe261a5f-630c-404e-ac18-8429d246000e?directory_alias=DataEngineering-QuickSight-Dashboard
