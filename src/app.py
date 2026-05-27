import traceback
import response as response
import modify_input as modify_input
from get_history import get_history
from add_transactions import add_transactions
from email import message_from_bytes
import base64

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
        if event.get("pathParameters", {}).get("add_transaction_action") == 'bulk_upload':
            content_type = event["headers"].get("content-type") or event["headers"].get("Content-Type")
            body = event.pop("body")

            # Decode base64
            if event.get("isBase64Encoded", False):
                body = base64.b64decode(body)
            else:
                body = body.encode()

            file_content = None

            # Handle multipart/form-data
            if content_type and "multipart/form-data" in content_type:
                # Add fake headers so email parser can understand
                full_message = b"Content-Type: " + content_type.encode() + b"\n\n" + body
                msg = message_from_bytes(full_message)

                for part in msg.walk():
                    content_disposition = part.get("Content-Disposition", "")
                    if "filename=" in content_disposition:
                        file_content = part.get_payload(decode=True)
                        break

                if not file_content:
                    raise Exception("File not found in multipart data")

            else:
                file_content = body
        else:
            event['body'] = base64.b64decode(event['body']).decode("utf-8")
        input_data, headers = modify_input.input_data(event)
        add_transaction_action = input_data.get('add_transaction_action')
        if add_transaction_action == 'bulk_upload':
            input_data['file_content'] = file_content
        result = add_transactions(input_data, add_transaction_action, headers)
        return response.create_response(200, result)
    except Exception as exp:
        print(traceback.format_exc())
        return response.create_response(400, str(exp))

