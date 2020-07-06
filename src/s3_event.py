import boto3
import sys
import json
from pygments import highlight, lexers, formatters
from src.s3_event_config import S3EventConfig, TopicConfig, QueueConfig, LambdaConfig

class S3Events:
    def __init__(self, client):
        self.Config = {}
        self.Client = client

    def __str__(self, pretty=True):
        json_txt = json.dumps((self.Config), indent = 4)
        if pretty is True:
            json_txt = highlight(
                json_txt,
                lexers.JsonLexer(),
                formatters.TerminalFormatter()
            )
        return(json_txt)

    # Update client object
    def update_client(self, client):
        self.Client = client
        return(self)

    def get_bucket_notifications(self, bucket_name):
        self.Config = self.Client.get_bucket_notification_configuration(
            Bucket=bucket_name
        )
        self.ResponseMetadata = self.Config.pop('ResponseMetadata', None)

    # Add notification to an existing configuration
    def add_notification_config(
        self, notif_type, dest_arn, events, 
        id=None, filter_prefix=None, filter_suffix=None, verbose=False
    ):
        config_params = {
            'id': id,
            'dest_arn': dest_arn,
            'events': events,
            'filter_prefix': filter_prefix,
            'filter_suffix': filter_suffix
        }

        notif_type_map = {
            'topic': TopicConfig(config_params),
            'queue': QueueConfig(config_params),
            'lambda': LambdaConfig(config_params)
        }
        if notif_type not in notif_type_map:
            raise ValueError("Invalid notif_type: {}. Valid types: [\"topic\",\"queue\",\"lambda\"]".format(notif_type))
        notif_config = notif_type_map[notif_type]

        # notif_config = TopicConfig(config_params)
        notif_config.construct_config()
        self.Config = notif_config.attach_config(self.Config)

        print("Config {} added".format(id))

    # Remove notification by Id
    def remove_notification(self, id):
        print("This method currently does nothing!")
        pass

    def put_notification(self, bucket_name):
        response = self.Client.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration=self.Config
        )

        return(response)


