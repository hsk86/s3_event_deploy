# CRUDdy S3 event deployments
Deployment of event configs on existing S3 buckets made (hopefully) simpler. BYO boto3 client object!

## What?
Convenient wrappers and helper functions around managing AWS S3 event configurations with boto3.

## Why?
A certain dev needed to deploy S3 event configs as an essential component of an event-driven data pipeline deployed via AWS SAM. As CloudFormation/SAM couldn't allow deployment of S3 event configs on an existing bucket, this left the dev to resort to Python + boto3. Few hours later, the dev was flabbergasted at the amount of boilerplate code required to perform a very simple task of updating S3 event configuration of an existing bucket.

## How?

### Instantiate
Pass in a [boto3 S3 client object](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client) to instantiate the object:

```python
from src.s3_event import S3Events
import boto3

# Change this to how the connection to your AWS environment is configured
client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN
)
conf = S3Events(client)
```

### Extract current S3 config
Notification configurations from an existing S3 bucket can be pulled with `get_bucket_notifications`

```python
conf.get_bucket_notifications(bucket_name='my-s3-bucket')
```

### Add new S3 config
Just set params and let `add_notification_config` deal with the rest!

Supports `notif_type`s: `"topic"`, `"queue"`, `"lambda"`

```python
conf.add_notification_config(
    notif_type='topic',
    id='my-new-topic',
    dest_arn='arn:aws:sns:ap-southeast-2:123456789012:MyTopic',
    events=['s3:ReducedRedundancyLostObject', 's3:ObjectCreated:*'],
    filter_prefix='images/',
    filter_suffix='.jpg'
)
```

### Remove S3 config
```python
conf.remove_notification_config(
    id='my-new-topic'
)
```

### Put to S3
```python
conf.put_notification(bucket_name='my-s3-bucket')
```

## What next?
- Extend this functionality to other S3 configurations, most of which works similarly to S3 event notifications.
- Add functionality to add raw JSON as an accepted input
- Make it easy to integrate this as a part of a [Lambda CustomResource](https://aws.amazon.com/premiumsupport/knowledge-center/cloudformation-s3-notification-lambda/). The value-add of this is extending the ability to handle deployments on buckets with existing event configs.