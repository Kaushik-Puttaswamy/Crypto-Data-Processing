# Crypto Data Processing and Analysis Pipeline Using AWS Glue, Kinesis, DynamoDB, Athena and QuickSight

## 📌 Project Overview

The Crypto Data Processing Pipeline is an end-to-end data processing solution designed to handle cryptocurrency transactions in real time. It leverages AWS Glue, AWS Lambda, Kinesis Firehose, DynamoDB Streams, and Hudi for efficient ETL and analytics. The project processes raw transaction data, performs transformations, categorizes trades based on risk, and stores processed data in an S3-based Hudi table for further analysis uisng AWS QucikSight.

## 📂 Project Structure

Crypto-Data-Processing/

│── crypto_nrt_etl_glue_job.py               # AWS Glue ETL script for data transformation & storage

│── lambda_transformer.py                     # AWS Lambda function for processing DynamoDB Streams

│── mock_crypto_data_to_dynamodb.py           # Script to simulate crypto transactions and insert them into DynamoDB

│── Project Execution Screenshots/            # Folder containing setup and execution screenshots

│── Project architecture                      # High-level architecture and data flow

└── README.md                                 # Project documentation (this file)































https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/78dd677e-34d1-4a4f-9b78-82a2f97863ba/views/fe261a5f-630c-404e-ac18-8429d246000e?directory_alias=DataEngineering-QuickSight-Dashboard
