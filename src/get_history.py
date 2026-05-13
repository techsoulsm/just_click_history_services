import helper
from boto3.dynamodb.conditions import Key, Attr


def get_history_decorator(function):

    def wrapper(*args, **kargs):
        history_table = helper.get_table('justclick_history')

        def user_id(*args, **kargs):
            input_data = args[0]
            manditory_fields = ['user_id']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            response = history_table.query(
                KeyConditionExpression=Key('user_id').eq(input_data['user_id']))['Items']
            return response

        def timestamp(*args, **kargs):
            input_data = args[0]
            manditory_fields = ['user_id', 'end_timestamp']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            response = history_table.query(
                KeyConditionExpression=Key('user_id').eq(input_data['user_id']),
                FilterExpression=Attr('timestamp').gt(input_data.get('start_timestamp', 0)) & Attr('end_timestamp').lt(input_data['end_timestamp'])
            )['Items']
            return response    

        allowed_operations = {'user_id': user_id, 'timestamp': timestamp}
        if args[1] not in allowed_operations:
            return f"provide one of the valid actions : {allowed_operations.keys()}"
        return allowed_operations[args[1]](*args, **kargs)

    return wrapper


@get_history_decorator
def get_history(input_data, get_history_by, headers):
    return input_data, get_history_by, headers
