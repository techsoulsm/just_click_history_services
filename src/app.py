import traceback
import response as response
import modify_input as modify_input

def lambdaHandler(event, context):
    try:
        input_data, headers = modify_input.input_data(event)
        action = input_data.get('action')
        result = {}
        return response.create_response(200, result)
    except Exception as exp:
        print(traceback.format_exc())
        return response.create_response(400, str(exp))


