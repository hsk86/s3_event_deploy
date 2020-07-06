# S3 Event Configs
Deployment of event configs on existing S3 buckets made (hopefully) simpler. BYO boto3 client object!

## What?
Convenient wrappers and helper functions around managing AWS S3 event configurations with boto3.

## Why?
A certain dev needed to deploy S3 event configs as an essential component of an event-driven data pipeline deployed via AWS SAM. As CloudFormation/SAM couldn't allow deployment of S3 event configs on an existing bucket, this left the dev to resort to Python + boto3. Few hours later, the dev was flabbergasted at the amount of boilerplate code required to perform a very simple task of updating S3 event configuration of an existing bucket.

## How?
Example deployment coming soon!

## What next?
- Extend this functionality to other S3 configurations, most of which works similarly to S3 event notifications.
- Add functionality to add raw JSON as an accepted input
- Make it easy to integrate this as a part of a [Lambda CustomResource](https://aws.amazon.com/premiumsupport/knowledge-center/cloudformation-s3-notification-lambda/). The value-add of this is extending the ability to handle deployments on buckets with existing event configs.