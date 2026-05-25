import boto3


def get_table(table_name):
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(table_name)

def check_is_user_admin(user_id):
    users_table = get_table(Constant.USERS_TABLE_NAME)
    response = users_table.get_item(Key={'cognitoId': user_id})
    if 'Item' not in response:
        raise Exception("User not found")
    return response['Item'].get('isAdmin')

class Constant:
    HISTORY_TABLE_NAME = 'justclick_history'
    USERS_TABLE_NAME = 'justclick_advertisements_users'
    HISTORY_TABLE_HASH_KEY = 'user_id'
    HISTORY_TABLE_RANGE_KEY = 'unique_id'
    HISTORY_TABLE_TRANSACTIONS_INDEX_NAME = 'transaction_id_index'
    HISTORY_TABLE_TRANSACTIONS_INDEX_HASH_KEY = 'transaction_id'