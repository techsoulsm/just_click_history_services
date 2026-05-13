import traceback
import response as response
import modify_input as modify_input
from get_history import get_history

def getHistory(event, context):
    try:
        input_data, headers = modify_input.input_data(event)
        get_history_by = input_data.get('get_history_by')
        result = get_history(input_data, get_history_by, headers)
        return response.create_response(200, result)
    except Exception as exp:
        print(traceback.format_exc())
        return response.create_response(400, str(exp))
