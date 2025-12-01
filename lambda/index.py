import json
import os
import csv
import random
import boto3
from datetime import datetime
from decimal import Decimal

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('QUOTES_TABLE_NAME')
table = dynamodb.Table(table_name)

def load_quotes_from_csv():
    """Load quotes from CSV file into DynamoDB"""
    try:
        # Check if table already has data
        response = table.scan(Limit=1)
        if response['Count'] > 0:
            print("Table already has data, skipping CSV load")
            return

        # Read CSV file and load into DynamoDB
        csv_path = os.path.join(os.path.dirname(__file__), 'quotes.csv')
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                table.put_item(
                    Item={
                        'id': row['id'],
                        'quote': row['quote'],
                        'author': row['author']
                    }
                )
        print(f"Successfully loaded quotes from CSV into {table_name}")
    except Exception as e:
        print(f"Error loading quotes from CSV: {str(e)}")
        raise

def get_random_quote():
    """Get a random quote from DynamoDB"""
    try:
        # Scan the table to get all quotes
        response = table.scan()
        items = response.get('Items', [])

        if not items:
            # If table is empty, load from CSV first
            load_quotes_from_csv()
            response = table.scan()
            items = response.get('Items', [])

        if items:
            # Select a random quote
            random_quote = random.choice(items)
            return random_quote
        else:
            return None
    except Exception as e:
        print(f"Error getting random quote: {str(e)}")
        raise

def handler(event, context):
    try:
        # Get a random quote
        quote_data = get_random_quote()

        if quote_data:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'quote': quote_data['quote'],
                    'author': quote_data['author'],
                    'timestamp': datetime.now().isoformat(),
                    'student_id': '9026254'
                })
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'No quotes found',
                    'timestamp': datetime.now().isoformat()
                })
            }
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            })
        }