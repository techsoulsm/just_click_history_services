import boto3


def get_table(table_name):
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(table_name)

def check_is_user_admin(user_id):
    users_table = get_table('justclick_advertisements_users')
    response = users_table.get_item(Key={'cognitoId': user_id})
    if 'Item' not in response:
        raise Exception("User not found")
    return response['Item'].get('isAdmin')