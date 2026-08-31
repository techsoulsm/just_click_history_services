import traceback
from helper import get_table
from datetime import datetime, timedelta
from dynamodb_json import json_util


def transactions_listener_handler(event, context):
    try:
        alerts_table = get_table(Constant.ALERTS_TABLE_NAME)
        for record in event['Records']:
            if record['eventName'] == 'INSERT':
                new_item = json_util.loads(record['dynamodb'].get('NewImage', {}))
                alert_record = generate_alert_record(new_item, 'TRANSACTION', 'New transaction has been added')
            elif record['eventName'] == 'MODIFY':
                new_item = json_util.loads(record['dynamodb'].get('NewImage', {}))
                alert_record = generate_alert_record(new_item, 'TRANSACTION', 'Transaction has been modified')

            alerts_table.put_item(Item=alert_record)
    except Exception as exp:
        print(traceback.format_exc())

def generate_alert_record(transaction, alert_type, description):
    now = datetime.now()
    timestamp = int(now.timestamp()*1000)
    ttl_date = now + timedelta(days=90)
    ttl_timestamp = int(ttl_date.timestamp())
    alert_record = {
        Constant.ALERTS_TABLE_HASH_KEY: transaction[Constant.ALERTS_TABLE_HASH_KEY],
        Constant.ALERTS_TABLE_RANGE_KEY: timestamp,
        Constant.ALERTS_TYPE: alert_type,
        'ttl': ttl_timestamp,
        'is_read': False,
        'description': description,
        'stage_name': transaction.get('stage_name', ''),
        'transaction_id': transaction.get('transaction_id', '')
    }
    return alert_record

class Constant:
    ALERTS_TABLE_NAME = 'justclick_alert_manager'
    ALERTS_TABLE_HASH_KEY = 'user_id'
    ALERTS_TABLE_RANGE_KEY = 'alert_id'
    ALERTS_TYPE = 'alert_type'