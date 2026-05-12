import json
from decimal import Decimal

""""
This will modify the all the input data to the single json
"""


# take the input data from the post man
def input_data(event):
    path_params = event.get("pathParameters", {})
    headers = event.get("headers", {})
    query_params = event.get("queryStringParameters", {})
    body = json.loads(event.get("body")) if event.get("body") else {}
    result = {}
    if event.get('requestContext'):
        result['stage_name'] = event.get('requestContext', {}).get('stage')
    result.update(path_params if path_params else {})
    result.update(query_params if query_params else {})
    # result.update(headers if headers else {})
    result.update(body if body else {})
    return result, headers


# decimal encoder
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


def is_valid(data: dict, validation_list: list):
    print('called is_valid method... with validation-list')
    print(validation_list)
    keys = validation_list
    for i in keys:
        if i not in data or data[i] is None or data[i] == "":
            print("key missing ")
            print(i)
            return i
        if isinstance(data[i], (list, dict, tuple)):
            if len(data[i]) == 0:
                print("list/dict key missing ")
                print(i)
                return i
    return True
