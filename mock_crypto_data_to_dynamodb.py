# ==============================
#  INSTALL REQUIRED LIBRARIES
# ==============================
# pip install boto3
# pip install faker

import boto3
import uuid
import random
import time
from datetime import datetime
from faker import Faker
from decimal import Decimal

# Initialize Faker library for generating random user data
fake = Faker()

# ==============================
#  AWS DYNAMODB CONFIGURATION
# ==============================

# Create a DynamoDB resource instance
dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")

# Specify the DynamoDB table name
table_name = "CryptoTransactions"
table = dynamodb.Table(table_name)

# ==============================
#  PREDEFINED MOCK DATA VALUES
# ==============================

# List of available cryptocurrency exchanges
EXCHANGES = ["Binance", "Coinbase", "Kraken", "FTX", "OKX", "Bitfinex"]

# List of common trading pairs
TRADING_PAIRS = ["BTC/USD", "ETH/USDT", "SOL/USD", "ADA/USDT", "XRP/USD"]

# Possible order types
ORDER_TYPES = ["BUY", "SELL"]

# Trade status categories
TRADE_STATUSES = ["SUCCESS", "FAILED", "PENDING"]

# Order source categories
ORDER_SOURCES = ["Web", "Mobile", "API"]

# ==============================
#  FUNCTION: GENERATE MOCK TRANSACTION
# ==============================

def generate_mock_transaction():
    """
    Generates a mock cryptocurrency transaction with realistic attributes.

    :return: A dictionary representing a crypto transaction.
    """
    return {
        "transaction_id": str(uuid.uuid4()),  # Unique transaction identifier
        "timestamp": datetime.utcnow().isoformat(),  # UTC timestamp of the trade
        "exchange": random.choice(EXCHANGES),  # Randomly select an exchange
        "trading_pair": random.choice(TRADING_PAIRS),  # Randomly select a trading pair
        "order_type": random.choice(ORDER_TYPES),  # Either BUY or SELL
        "price": Decimal(str(round(random.uniform(100, 70000), 2))),  # Random price (float → Decimal)
        "quantity": Decimal(str(round(random.uniform(0.01, 5), 6))),  # Random quantity (float → Decimal)
        "trade_fee": Decimal(str(round(random.uniform(0.01, 1), 4))),  # Trade fee amount (float → Decimal)
        "trade_status": random.choice(TRADE_STATUSES),  # Trade status (SUCCESS, FAILED, PENDING)
        "user_id": fake.uuid4(),  # Fake user ID
        "wallet_address": fake.iban(),  # Generate a fake wallet address (using IBAN format)
        "order_source": random.choice(ORDER_SOURCES),  # Order source (Web, Mobile, API)
    }

# ==============================
#  FUNCTION: INSERT TRANSACTION INTO DYNAMODB
# ==============================

def publish_transaction():
    """
    Generates and inserts a mock transaction into the DynamoDB table.

    :return: Response from DynamoDB put_item operation.
    """
    transaction = generate_mock_transaction()  # Generate a mock transaction
    response = table.put_item(Item=transaction)  # Insert transaction into DynamoDB
    print(f"Inserted transaction: {transaction}")  # Log the inserted transaction
    return response

# ==============================
#  MAIN EXECUTION: CONTINUOUSLY PUBLISH TRANSACTIONS
# ==============================

if __name__ == "__main__":
    while True:
        publish_transaction()  # Insert a new transaction into DynamoDB
        time.sleep(random.randint(1, 5))  # Wait for a random interval (1-5 seconds)