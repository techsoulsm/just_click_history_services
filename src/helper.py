import io
import boto3
import requests
import pandas as pd


def get_table(table_name):
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(table_name)

def check_is_user_admin(user_id):
    users_table = get_table(Constant.USERS_TABLE_NAME)
    response = users_table.get_item(Key={'cognitoId': user_id})
    if 'Item' not in response:
        raise Exception("User not found")
    return response['Item'].get('isAdmin')

def get_cognito_id_by_email(email, stage):
    authentication_api_url = get_authentication_api(stage)
    authentication_api_url = authentication_api_url.replace("{action}", Constant.FETCH_COGNITO_ID_ACTION)
    response = requests.post(authentication_api_url, json={'email': email})
    if response.status_code != 200:
        raise Exception("Error fetching cognito id")
    return response.json()

def get_authentication_api(stage):
    configurations_table = get_table(Constant.CONFIGURATIONS_TABLE_NAME)
    response = configurations_table.get_item(Key={Constant.CONFIGURATIONS_TABLE_HASH_KEY: Constant.CONFIGURATIONS_TABLE_HASH_VALUE,
                                                  Constant.CONFIGURATIONS_TABLE_RANGE_KEY: f"{stage}_{Constant.CONFIGURATIONS_TABLE_RANGE_VALUE}"})
    return response['Item'].get('url_arn')

def read_excel(file):
    df = pd.read_excel(io.BytesIO(file))
    for column in ['email', 'transaction_id', 'payment_amount', 'payment_date']:
        if column not in df.columns:
            raise Exception(f"please provide {column}")
    return df.to_dict(orient='records')

class Constant:
    HISTORY_TABLE_NAME = 'justclick_history'
    USERS_TABLE_NAME = 'justclick_advertisements_users'
    HISTORY_TABLE_HASH_KEY = 'user_id'
    HISTORY_TABLE_RANGE_KEY = 'unique_id'
    HISTORY_TABLE_TRANSACTIONS_INDEX_NAME = 'transaction_id_index'
    HISTORY_TABLE_TRANSACTIONS_INDEX_HASH_KEY = 'transaction_id'
    CONFIGURATIONS_TABLE_NAME = 'configurationDNS'
    CONFIGURATIONS_TABLE_HASH_KEY = 'configurationName'
    CONFIGURATIONS_TABLE_RANGE_KEY = 'configurationGroup'
    CONFIGURATIONS_TABLE_HASH_VALUE = 'All'
    CONFIGURATIONS_TABLE_RANGE_VALUE = 'authentication_api_details'
    FETCH_COGNITO_ID_ACTION = 'fetch_cognito_id_by_email'