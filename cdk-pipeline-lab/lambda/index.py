import json
from datetime import datetime

def handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello from Lambda! After triggering redeployment',
            'timestamp': datetime.now().isoformat()
        })
    }