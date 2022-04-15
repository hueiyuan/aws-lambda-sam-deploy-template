import os
import json
import ast
import logging

from cachetools import TTLCache
from slack_sdk.webhook import WebhookClient

import utils
from config import SlackConfig

ENV = os.environ['ENV']
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
DAILY_EXCEPTION_CACHE = TTLCache(maxsize=10, ttl=86400)

SLACK_CONFIG = SlackConfig()
SLACK_TOKEN = utils.get_ssm_value(
    region='ap-northeast-1', 
    ssm_name=SLACK_CONFIG.ssm_slack_token
)

def sent_slack_alert(exception_side, exception_type, s3_path):
    webhook = WebhookClient(
        url=os.path.join(
            SLACK_CONFIG.slack_webhook_prefix_url, 
            SLACK_TOKEN
        )
    )
    
    alert_message_body = [
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f":bangbang: Exception Type: `{exception_type}` \nS3 Folder: `{s3_path}`"
                }
            ]
        }
    ]
    
    response = webhook.send(
        text="fallback", 
        blocks=alert_message_body
    )

    
def lambda_handler(event, context):
    s3_event = ast.literal_eval(event['Records'][0]['body'])
    s3_bucket = s3_event['Records'][0]['s3']['bucket']['name']
    s3_key = s3_event['Records'][0]['s3']['object']['key']
    s3_key_list = s3_key.split(exception_side)[-1].split('/')[1:-1]
    s3_path = 's3://{}/{}'.format(s3_bucket, prefix_folder)
    prefix_folder = '/'.join(s3_key_list)
    exception_type = s3_key_list[0]
    
    try:
      sent_slack_alert(exception_type, s3_path)
    except Exception as e:
      logger.exception(e)
      raise  ## for retry process
      
