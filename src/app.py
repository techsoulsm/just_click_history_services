import base64
import traceback
import response as response
import modify_input as modify_input
from get_history import get_history
from add_transactions import add_transactions

def getHistory(event, context):
    try:
        input_data, headers = modify_input.input_data(event)
        get_history_action = input_data.get('get_history_action')
        result = get_history(input_data, get_history_action, headers)
        return response.create_response(200, result)
    except Exception as exp:
        print(traceback.format_exc())
        return response.create_response(400, str(exp))
    
def add_transaction(event, context):
    try:
        file_content = None
        if event.get("pathParameters", {}).get("add_transaction_action") == 'bulk_upload':
            file_content = event.pop('body')
            if event.get('isBase64Encoded'):
                file_content = base64.b64decode(file_content)
            else:
                # If API Gateway passes raw text, keep bytes for Excel parsing.
                file_content = file_content.encode('utf-8')
        input_data, headers = modify_input.input_data(event)
        add_transaction_action = input_data.get('add_transaction_action')
        if add_transaction_action == 'bulk_upload':
            input_data['file_content'] = file_content
        result = add_transactions(input_data, add_transaction_action, headers)
        return response.create_response(200, result)
    except Exception as exp:
        print(traceback.format_exc())
        return response.create_response(400, str(exp))

