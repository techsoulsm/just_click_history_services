from typing import Union, List, Dict
import json
from decimal import Decimal


# creating responce
def create_response(status_code: int, body: Union[dict, list, str], **kwargs):
    return {'statusCode': status_code,
            'body': json.dumps(body, default=kwargs.get('default'), cls=DecimalEncoder),
            'headers': {
                'Access-Control-Allow-Headers': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
            }}


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)
