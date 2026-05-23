import helper
from boto3.dynamodb.conditions import Key, Attr
import base64
import json
from decimal import Decimal
import time


def get_history_decorator(function):

    def wrapper(*args, **kargs):
        history_table = helper.get_table('justclick_history')

        def get_transactions_by_user(*args, **kargs):
            input_data = args[0]
            manditory_fields = ['user_id']
            limit = int(input_data.get('limit', 50))
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            if 'LastEvaluatedKey' in input_data:
                query_response = history_table.query(
                    KeyConditionExpression=Key('user_id').eq(input_data['user_id']),
                    ScanIndexForward=True,
                    Limit=limit,
                    ExclusiveStartKey=json.loads(base64.b64decode(input_data['LastEvaluatedKey']).decode('utf-8'))
                )
            else:
                query_response = history_table.query(
                    KeyConditionExpression=Key('user_id').eq(input_data['user_id']),
                    ScanIndexForward=True,
                    Limit=limit
                )
            results = {}
            results['Items'] = query_response['Items']
            if 'LastEvaluatedKey' in query_response:
                results['LastEvaluatedKey'] = base64.b64encode(
                    json.dumps(query_response.get('LastEvaluatedKey'), cls=DecimalEncoder).encode('utf-8')
                ).decode('utf-8')
            return results

        def get_transactions_by_timestamp(*args, **kargs):
            input_data = args[0]
            manditory_fields = ['user_id']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            start_timestamp = int(input_data.get('start_timestamp', 0))
            end_timestamp = int(input_data.get('end_timestamp', time.time()))
            limit = int(input_data.get('limit', 50))
            if 'LastEvaluatedKey' in input_data:
                if helper.check_is_user_admin(input_data['user_id']).lower() == 'true':
                    query_response = history_table.scan(
                        FilterExpression=Key('unique_id').between(start_timestamp, end_timestamp),
                        ScanIndexForward=True,
                        Limit=limit,
                        ExclusiveStartKey=json.loads(base64.b64decode(input_data['LastEvaluatedKey']).decode('utf-8'))
                    )
                else:
                    query_response = history_table.query(
                        KeyConditionExpression=Key('user_id').eq(input_data['user_id']) & Key('unique_id').between(start_timestamp, end_timestamp),
                        ScanIndexForward=True,
                        Limit=limit,
                        ExclusiveStartKey=json.loads(base64.b64decode(input_data['LastEvaluatedKey']).decode('utf-8'))
                    )
            else:
                if helper.check_is_user_admin(input_data['user_id']).lower() == 'true':
                    query_response = history_table.scan(
                        FilterExpression=Key('unique_id').between(start_timestamp, end_timestamp),
                        ScanIndexForward=True,
                        Limit=limit
                    )
                else:
                    query_response = history_table.query(
                        KeyConditionExpression=Key('user_id').eq(input_data['user_id']) & Key('unique_id').between(start_timestamp, end_timestamp),
                        ScanIndexForward=True,
                        Limit=limit
                    )
            results = {}
            results['Items'] = query_response['Items']
            if 'LastEvaluatedKey' in query_response:
                results['LastEvaluatedKey'] = base64.b64encode(
                    json.dumps(query_response.get('LastEvaluatedKey'), cls=DecimalEncoder).encode('utf-8')
                ).decode('utf-8')
            return results    

        def get_transaction_by_id(*args, **kargs):
            input_data = args[0]
            manditory_fields = ['user_id', 'transaction_id']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            response = history_table.query(
                KeyConditionExpression=Key('user_id').eq(input_data['user_id']),
                FilterExpression=Attr('transaction_id').eq(input_data['transaction_id'])
            )['Items']
            return response
        
        def get_last_transaction_by_user(*args, **kargs):
            input_data = args[0]
            manditory_fields = ['user_id']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            response = history_table.query(
                KeyConditionExpression=Key('user_id').eq(input_data['user_id']),
                ScanIndexForward=False,
                Limit=1
            )['Items']
            return response
        
        def get_total_transactions_by_user(*args, **kargs):
            input_data = args[0]
            manditory_fields = ['user_id', 'end_timestamp']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            response = history_table.query(
                KeyConditionExpression=Key('user_id').eq(input_data['user_id']) & Key('unique_id').between(int(input_data.get('start_timestamp', 0)),int(input_data['end_timestamp'])),
                Select='COUNT'
            )['Count']
            return response

        allowed_operations = {'get_transactions_by_user': get_transactions_by_user, 'get_transactions_by_timestamp': get_transactions_by_timestamp, 'get_transaction_by_id': get_transaction_by_id, 
                              'get_last_transaction_by_user': get_last_transaction_by_user, 'get_total_transactions_by_user': get_total_transactions_by_user}
        if args[1] not in allowed_operations:
            return f"provide one of the valid actions : {allowed_operations.keys()}"
        return allowed_operations[args[1]](*args, **kargs)

    return wrapper


@get_history_decorator
def get_history(input_data, get_history_action, headers):
    return input_data, get_history_action, headers


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)
