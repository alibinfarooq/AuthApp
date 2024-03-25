import boto3
import json

def lambda_handler(event, context):
    # The event parameter contains data about the event that triggered the Lambda function
    # The context parameter provides runtime information about the Lambda function
    # For simplicity, we're not using these parameters in this example

    # Define the message
    message = "Hello, world!"

    # Return the message
    return {
        'statusCode': 200,  # HTTP status code indicating success
        'body': message     # Response body containing the message
    }