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

## ✅  Prerequisites

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

![Project Architecture .png](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline-Using-AWS-Glue-Kinesis-DynamoDB-Athena-and-QuickSight/blob/main/Project%20Architecture%20.png)

### Data Flow:

• 1, Mock data generator → DynamoDB

• 2, 3, DynamoDB Stream → Kinesis Firehose

• 4, Firehose → Lambda (Transformation)

• 5, 6, 7, 8, 9, Raw S3 → Glue ETL (Hudi Processing)

• 10, 11, Processed S3 → Athena → QuickSight


This project follows a real-time data ingestion and processing pipeline:
	
1. Data Generation (Mock Transactions)

	• A Python script (mock_crypto_data_to_dynamodb.py) continuously generates mock crypto transactions.

	• The data is inserted into AWS DynamoDB.

2. Data Streaming & Transformation

	• DynamoDB Streams captures changes and forwards them to AWS Kinesis Firehose.

	• A Lambda function (lambda_transformer.py) transforms the data from DynamoDB’s format to JSON.
	
3. Real-Time ETL Processing (AWS Glue)

	• AWS Glue reads data from S3 (landing zone).

	• Performs data transformations, including:

	• Risk flagging based on trade value.

	• Price normalization across exchanges.

	• Fee adjustments based on transaction size.

	• User categorization based on trade volume.

	• Writes processed data into an AWS S3-based Hudi table.
	
4. Data Storage & Analytics

	• Processed Data: Stored in an S3 Hudi table (processed_crypto_txn).

	• Querying: AWS Athena is used to query Hudi tables.

	• Visualization: QuickSight dashboards are built on Athena queries.

## 🛠 Setup & Execution Steps

Step 1: Configure AWS DynamoDB

• Create a DynamoDB Table (CryptoTransactions).

• Enable DynamoDB Streams to capture changes.

📌 Screenshot: DynamoDB_Table_Setup_with_Data_stream_and_CDC_enabled.png

![DynamoDB_Table_Setup_with_Data_stream_and_CDC_enabled](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/DynamoDB_Table_Setup_with_Data_stream_and_CDC_enabled.png?raw=true)

Step 2: Setup AWS Kinesis Firehose
	
 • Create a Kinesis Firehose delivery stream.
	
 • Configure Firehose to read from DynamoDB Streams and deliver data to S3.

📌 Screenshot: Firehose_Stream_Setup.png

![Firehose_Stream_Setup.png](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/Firehose_Stream_Setup.png?raw=true)

📌 Screenshot: Kinesis_Setup_with_Shard_Showing_Records.png

![Kinesis_Setup_with_Shard_Showing_Records](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/Kinesis_Setup_with_Shard_Showing_Records.png?raw=true)

Step 3: Create & Deploy AWS Lambda Function

• Deploy lambda_transformer.py to process data from Kinesis Firehose.

• This function:
	
 • Converts DynamoDB JSON format into standard JSON.
	
 • Adds metadata (event type, timestamp, event ID).
	
 • Outputs transformed data to Kinesis Firehose.

📌 Screenshot: Lambda_Function_for_Data_Transformation.png

![Lambda_Function_for_Data_Transformation](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/Lambda_Function_for_Data_Transformation.png?raw=true)

📌 Screenshot: Lambda_Function_Permission_Policies.png

![Lambda_Function_Permission_Policies](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/Lambda_Function_Permission_Policies.png?raw=true)

Step 4: Setup AWS Glue for ETL
	
 • Create an AWS Glue Crawler to catalog data from S3 (Raw Transactions).
	
 • Define a Glue ETL Job to process data using crypto_nrt_etl_glue_job.py.
	
 • Glue ETL performs:
	
 • Data Transformation
	
 • Trade Risk Classification
	
 • Price Normalization
	
 • User Categorization
	
 • Hudi-based storage in S3


📌 Screenshot: Glue_Database_Setup.png

![Glue_Database_Setup.png](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/Glue_Database_Setup.png?raw=true)

📌 Screenshot: Glue_Table_for_Raw_Processed_Data.png

![Glue_Table_for_Raw_Processed_Data](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/Glue_Table_for_Raw_Processed_Data.png?raw=true)

📌 Screenshot: Glue_ETL_Setup.png

![Glue_ETL_Setup.png](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/Glue_ETL_Setup.png?raw=true)

📌 Screenshot: Glue_ETL_Job_Status.png

![Glue_ETL_Job_Status.png](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/Glue_ETL_Job_Status.png?raw=true)

Step 5: Query Data using AWS Athena
	
 • AWS Athena is used to run SQL queries on processed crypto transactions stored in Hudi tables.
	
 • Sample query:


``` select * from crypto.processed_crypto_txn limit 10; ```

``` select count(*) from crypto.processed_crypto_txn limit 10; ```

``` SELECT * FROM crypto.processed_crypto_txn WHERE risk_flag = 'MEDIUM_RISK'; ```

📌 Screenshot: Athena_Query_Execution_for_Processed_Data.png

![Athena_Query_Execution_for_Processed_Data](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/Athena_Query_Execution_for_Processed_Data.png?raw=true)

Step 6: Visualize Data using QuickSight
	
 • AWS QuickSight connects to Athena and visualizes trade risk trends, price normalization, and user activity.
	
 
 Insights include:

 • Trade Fee Collected
 
 • Exchange Comparison
	
 • Trading Volume per Trading Pair
	
 • Risk Distribution
	
 • Number of Trades by Status
 
 • Order Type Distribution
 
 • User Category Distribution

 📌 Screenshot: QuickSight_File_Screenshot.png
 
![QuickSight_File_Screenshot.png](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/QuickSight_File_Screenshot.png?raw=true)


📌 Screenshot: Crypto_Trading_Insights_Dashboard_using_QuickSight.png

![Crypto_Trading_Insights_Dashboard_using_QuickSight](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/Crypto_Trading_Insights_Dashboard_using_QuickSight.png?raw=true)

📎 link: https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/78dd677e-34d1-4a4f-9b78-82a2f97863ba/views/fe261a5f-630c-404e-ac18-8429d246000e?directory_alias=DataEngineering-QuickSight-Dashboard

Step 7: Automate Execution with AWS Triggers
	
 • Set up AWS Glue triggers to run ETL jobs automatically based on new data arrival.

📌 Screenshot: Trigger_Setup.png

![Trigger_Setup.png](https://github.com/Kaushik-Puttaswamy/Crypto-Data-Processing-and-Analysis-Pipeline/blob/main/Project%20Execution%20Screenshots/Trigger_Setup.png?raw=true)

## 🔥 Key Features & Enhancements

✅ Real-Time Processing: Uses DynamoDB Streams + Kinesis Firehose for event-driven processing.

✅ Risk-Based Classification: Flags transactions based on trade value.

✅ Price Normalization: Adjusts price across multiple exchanges for fair comparison.

✅ User Categorization: Identifies VIP Traders, Active Traders, and Casual Traders.

✅ Athena & QuickSight Analytics: Enables ad-hoc analysis and business intelligence dashboards.

✅ Efficient Storage with Hudi: Ensures incremental updates & faster queries using Apache Hudi.

## 🚀 How to Run Locally?

Step 1: Install Dependencies

Ensure you have Python 3.x and the required AWS libraries:

``` pip install boto3 faker ```

Step 2: Simulate Transactions (Mock Data)

Run the script to insert transactions into DynamoDB:

``` python mock_crypto_data_to_dynamodb.py ```

Step 3: Deploy AWS Resources
	
 1.	Deploy Lambda function (lambda_transformer.py).
	
 2.	Configure Kinesis Firehose and connect it to DynamoDB Streams.
	
 3.	Setup Glue Crawler & Glue ETL Job.

Step 4: Run AWS Glue ETL

Manually trigger the Glue ETL job:

``` aws glue start-job-run --job-name crypto_nrt_etl_glue_job ```

Step 5: Query & Analyze Data

Use AWS Athena or QuickSight to analyze processed data.

## 📌 Future Enhancements


🔹 Add Machine Learning Anomaly Detection for fraud detection.

🔹 Implement Kafka instead of Kinesis for higher scalability.

🔹 Support Multi-Region Data Processing for global transaction tracking.

🔹 Enhance Data Governance with AWS Lake Formation.

## 👤 Project Author
	
 • Kaushik Puttaswamy  - Aspiring Data Engineer (https://www.linkedin.com/in/kaushik-puttaswamy-data-analyst/)

📧 For queries, reach out at ```kaushik.p9699@gmail.com```

## 🎯 Conclusion

This project demonstrates real-time crypto transaction processing using AWS Glue, DynamoDB, and Apache Hudi. The system is scalable, efficient, and provides insights into high-risk transactions, exchange price variations, and trading behaviors.



