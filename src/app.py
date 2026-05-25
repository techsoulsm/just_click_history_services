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
        file_content = event['body']
        print(file_content)
        input_data, headers = modify_input.input_data(event)
        add_transaction_action = input_data.get('add_transaction_action')
        result = add_transactions(input_data, add_transaction_action, headers)
        return response.create_response(200, result)
    except Exception as exp:
        print(traceback.format_exc())
        return response.create_response(400, str(exp))

