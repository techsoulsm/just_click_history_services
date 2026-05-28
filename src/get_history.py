import helper
from boto3.dynamodb.conditions import Key, Attr
import base64
import json
from decimal import Decimal
import time


def get_history_decorator(function):

    def wrapper(*args, **kargs):
        constants = helper.Constant()
        history_table = helper.get_table(constants.HISTORY_TABLE_NAME)

        def get_transactions_by_user(*args, **kargs):
            print("get_transactions_by_user called")
            input_data = args[0]
            manditory_fields = ['user_id']
            limit = int(input_data.get('limit', 50))
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            if 'LastEvaluatedKey' in input_data:
                query_response = history_table.query(
                    KeyConditionExpression=Key(constants.HISTORY_TABLE_HASH_KEY).eq(input_data['user_id']),
                    ScanIndexForward=True,
                    Limit=limit,
                    ExclusiveStartKey=json.loads(base64.b64decode(input_data['LastEvaluatedKey']).decode('utf-8'))
                )
            else:
                query_response = history_table.query(
                    KeyConditionExpression=Key(constants.HISTORY_TABLE_HASH_KEY).eq(input_data['user_id']),
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
            print("get_transactions_by_timestamp called")
            input_data = args[0]
            manditory_fields = ['user_id']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            start_timestamp = int(input_data.get('start_timestamp', 0))
            end_timestamp = int(input_data.get('end_timestamp', time.time() * 1000))
            limit = int(input_data.get('limit', 50))
            if 'LastEvaluatedKey' in input_data:
                if helper.check_is_user_admin(input_data['user_id']).lower() == 'true':
                    query_response = history_table.query(
                        IndexName=constants.HISTORY_TABLE_UNIQUE_ID_INDEX_NAME,
                        KeyConditionExpression=Key(constants.HISTORY_TABLE_UNIQUE_ID_INDEX_HASH_KEY).eq(input_data['stage_name']) & Key(constants.HISTORY_TABLE_UNIQUE_ID_INDEX_RANGE_KEY).between(start_timestamp, end_timestamp),
                        ScanIndexForward=True,
                        Limit=limit,
                        ExclusiveStartKey=json.loads(base64.b64decode(input_data['LastEvaluatedKey']).decode('utf-8'))
                    )
                else:
                    query_response = history_table.query(
                        KeyConditionExpression=Key(constants.HISTORY_TABLE_HASH_KEY).eq(input_data['user_id']) & Key(constants.HISTORY_TABLE_RANGE_KEY).between(start_timestamp, end_timestamp),
                        ScanIndexForward=True,
                        Limit=limit,
                        ExclusiveStartKey=json.loads(base64.b64decode(input_data['LastEvaluatedKey']).decode('utf-8'))
                    )
            else:
                if helper.check_is_user_admin(input_data['user_id']).lower() == 'true':
                    query_response = history_table.query(
                        IndexName=constants.HISTORY_TABLE_UNIQUE_ID_INDEX_NAME,
                        KeyConditionExpression=Key(constants.HISTORY_TABLE_UNIQUE_ID_INDEX_HASH_KEY).eq(input_data['stage_name']) & Key(constants.HISTORY_TABLE_UNIQUE_ID_INDEX_RANGE_KEY).between(start_timestamp, end_timestamp),
                        ScanIndexForward=True,
                        Limit=limit
                    )
                else:
                    query_response = history_table.query(
                        KeyConditionExpression=Key(constants.HISTORY_TABLE_HASH_KEY).eq(input_data['user_id']) & Key(constants.HISTORY_TABLE_RANGE_KEY).between(start_timestamp, end_timestamp),
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
            print("get_transaction_by_id called")
            input_data = args[0]
            manditory_fields = ['user_id', 'transaction_id']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            response = history_table.query(
                KeyConditionExpression=Key(constants.HISTORY_TABLE_HASH_KEY).eq(input_data['user_id']),
                FilterExpression=Attr(constants.HISTORY_TABLE_TRANSACTIONS_INDEX_HASH_KEY).eq(input_data['transaction_id'])
            )['Items']
            return response
        
        def get_last_transaction_by_user(*args, **kargs):
            print("get_last_transaction_by_user called")
            input_data = args[0]
            manditory_fields = ['user_id']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            response = history_table.query(
                KeyConditionExpression=Key(constants.HISTORY_TABLE_HASH_KEY).eq(input_data['user_id']),
                ScanIndexForward=False,
                Limit=1
            )['Items']
            return response
        
        def get_total_transactions_by_user(*args, **kargs):
            print("get_total_transactions_by_user called")
            input_data = args[0]
            manditory_fields = ['user_id']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            start_timestamp = int(input_data.get('start_timestamp', 0))
            end_timestamp = int(input_data.get('end_timestamp', time.time() * 1000))
            response = history_table.query(
                KeyConditionExpression=Key(constants.HISTORY_TABLE_HASH_KEY).eq(input_data['user_id']) & Key(constants.HISTORY_TABLE_RANGE_KEY).between(start_timestamp, end_timestamp),
                Select='COUNT'
            )['Count']
            return response
        
        def get_users(*args, **kargs):
            print("get_users called")
            input_data = args[0]
            if helper.check_is_user_admin(input_data['admin_id']).lower() != 'true':
                raise Exception("User is not an admin.")
            users_table = helper.get_table(constants.USERS_TABLE_NAME)
            limit = int(input_data.get('limit', 50))
            if 'LastEvaluatedKey' in input_data:
                query_response = users_table.query(
                    IndexName=constants.USERS_TABLE_STAGE_INDEX_NAME,
                    KeyConditionExpression=Key(constants.USERS_TABLE_STAGE_INDEX_HASH_KEY).eq(input_data['stage_name']),
                    Limit=limit,
                    ExclusiveStartKey=json.loads(base64.b64decode(input_data['LastEvaluatedKey']).decode('utf-8'))
                )
            else:
                query_response = users_table.query(
                    IndexName=constants.USERS_TABLE_STAGE_INDEX_NAME,
                    KeyConditionExpression=Key(constants.USERS_TABLE_STAGE_INDEX_HASH_KEY).eq(input_data['stage_name']),
                    Limit=limit
                )
            results = {}
            results['Items'] = query_response['Items']
            if 'LastEvaluatedKey' in query_response:
                results['LastEvaluatedKey'] = base64.b64encode(
                    json.dumps(query_response.get('LastEvaluatedKey'), cls=DecimalEncoder).encode('utf-8')
                ).decode('utf-8')
            return results

        allowed_operations = {'get_transactions_by_user': get_transactions_by_user, 'get_transactions_by_timestamp': get_transactions_by_timestamp, 'get_transaction_by_id': get_transaction_by_id, 
                              'get_last_transaction_by_user': get_last_transaction_by_user, 'get_total_transactions_by_user': get_total_transactions_by_user, 'get_users': get_users}
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
