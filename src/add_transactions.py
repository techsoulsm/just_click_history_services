import helper
from boto3.dynamodb.conditions import Key, Attr
import base64
import json
from decimal import Decimal
import time


def add_transactions_decorator(function):

    def wrapper(*args, **kargs):
        constants = helper.Constant()
        history_table = helper.get_table(constants.HISTORY_TABLE_NAME)

        def upload_transaction(*args, **kargs):
            print("upload_transaction called")
            input_data = args[0]
            manditory_fields = ['email', 'transaction_id', 'payment_amount', 'admin_id', 'payment_date']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            if helper.check_is_user_admin(input_data['admin_id']).lower() != 'true':
                raise Exception("Uploader is not an admin.")
            input_data['unique_id'] = int(time.time() * 1000)
            cognito_id = helper.get_cognito_id_by_email(input_data['email'], input_data.get('stage_name'))
            input_data['user_id'] = cognito_id
            dynamodb_response = history_table.put_item(Item=input_data)
            if dynamodb_response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise Exception("Error uploading transaction")
            return "Transaction uploaded successfully"
        
        def bulk_upload_transactions(*args, **kargs):
            print("bulk_upload_transactions called")
            input_data = args[0]
            manditory_fields = ['admin_id']
            for attribute in manditory_fields:
                if attribute not in input_data:
                    raise Exception(f"Please provide {attribute}")
            if helper.check_is_user_admin(input_data['admin_id']).lower() != 'true':
                raise Exception("Uploader is not an admin.")
            transactions = helper.read_excel(input_data['file_content'])
            
            for transaction in transactions:
                transaction['unique_id'] = int(time.time() * 1000)
                transaction['user_id'] = helper.get_cognito_id_by_email(transaction['email'], input_data.get('stage_name'))
                transaction['payment_date'] = str(transaction['payment_date'])
                transaction['stage_name'] = input_data.get('stage_name')
                history_table.put_item(Item=transaction)
            return "Transactions uploaded successfully"
        

        allowed_operations = {'upload': upload_transaction, 'bulk_upload': bulk_upload_transactions}
        if args[1] not in allowed_operations:
            return f"provide one of the valid actions : {allowed_operations.keys()}"
        return allowed_operations[args[1]](*args, **kargs)

    return wrapper


@add_transactions_decorator
def add_transactions(input_data, add_transaction_action, headers):
    return input_data, add_transaction_action, headers


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)
