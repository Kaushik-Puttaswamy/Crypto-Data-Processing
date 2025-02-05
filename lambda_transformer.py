import json
import base64

def dynamodb_json_to_dict(dynamodb_json):
    """
    Convert DynamoDB JSON format to a standard JSON format with correct data types.

    DynamoDB streams represent data in a specific JSON format where each value is stored 
    as a dictionary with a single key indicating its type (e.g., "S" for string, "N" for number).
    
    This function recursively converts those values into native Python types.
    
    :param dynamodb_json: Dictionary representing DynamoDB JSON format.
    :return: Dictionary with standard JSON types.
    """
    output = {}
    
    for key, value in dynamodb_json.items():
        if "S" in value:  # String type
            output[key] = value["S"]
        elif "N" in value:  # Number type (converted to float)
            output[key] = float(value["N"])
        elif "BOOL" in value:  # Boolean type
            output[key] = value["BOOL"]
        elif "NULL" in value:  # Null type
            output[key] = None
        elif "L" in value:  # List type (recursively convert if list contains objects)
            output[key] = [dynamodb_json_to_dict(i) if isinstance(i, dict) else i for i in value["L"]]
        elif "M" in value:  # Map type (recursively convert dictionary)
            output[key] = dynamodb_json_to_dict(value["M"])
        else:  # Other unhandled types (default to raw value)
            output[key] = value
            
    return output

def lambda_handler(event, context):
    """
    AWS Lambda function to process Kinesis Firehose records from a DynamoDB Stream.

    This function:
    - Decodes Base64-encoded Kinesis Firehose records.
    - Extracts and transforms DynamoDB "NewImage" data into standard JSON format.
    - Adds event metadata (eventName, eventID).
    - Re-encodes the transformed data in Base64 format for Firehose delivery.
    
    :param event: Dictionary containing batch records from AWS Kinesis Firehose.
    :param context: AWS Lambda execution context (not used in this function).
    :return: Dictionary containing transformed records.
    """
    transformed_records = []  # Store processed records

    for record in event["records"]:
        # Decode base64-encoded Kinesis data
        payload = base64.b64decode(record['data']).decode("utf-8")
        raw_data = json.loads(payload)
        
        # Check if the event contains a "NewImage" (latest item state from DynamoDB)
        if "dynamodb" in raw_data and "NewImage" in raw_data["dynamodb"]:
            # Convert DynamoDB JSON format to standard JSON
            transformed_data = dynamodb_json_to_dict(raw_data["dynamodb"]["NewImage"])
            
            # Add event metadata
            transformed_data["event_name"] = raw_data.get("eventName", "UNKNOWN")  # e.g., INSERT, MODIFY, REMOVE
            transformed_data["event_id"] = raw_data.get("eventID", "UNKNOWN")  # Unique event identifier
            
            # Convert transformed data to JSON string
            transformed_data_str = json.dumps(transformed_data) + '\n'
            
            # Encode the JSON string in Base64 (required for Firehose)
            transformed_data_encoded = base64.b64encode(transformed_data_str.encode('utf-8')).decode('utf-8')
            
            # Append transformed record to the output list
            transformed_records.append({
                'recordId': record['recordId'],  # Keep the original record ID
                'result': 'Ok',  # Indicate successful processing
                'data': transformed_data_encoded  # Store transformed data
            })

    # Return the processed records to Firehose
    return {
        "records": transformed_records
    }