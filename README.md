# Face Recognition with Actcast and Amazon Rekognition

This is a sample code to build a practical face recognition system combining [Actcast](https://actcast.io) and [Amazon Rekognition](https://aws.amazon.com/rekognition/).

Using Amazon Rekognition's API, you can easily build a face recognition system.
However, when analyzing real-world images captured by security cameras, etc., it is necessary to process a large number of images captured continuously, which incurs high network traffic costs and API usage fees.
Therefore, **an edge-cloud hybrid architecture** is required, where the first stage is analyzed on the edge and the second stage only when necessary on the cloud.

In this sample project, we use Raspberry Pi to detect and track faces on the edge, and calls Rekognition API only when it detects a person's face to turn it into a Face ID.

# actcast-rekognition-demo

This is a sample template for actcast-rekognition-demo - Below is a brief explanation of what we have generated for you:

```bash
.
├── README.md                   <-- This instructions file
├── func                        <-- Source code for a lambda function
│   ├── __init__.py
│   ├── app.py                  <-- Lambda function code
│   └── requirements.txt        <-- Python dependencies
└── template.yaml               <-- SAM Template
```

## Requirements

* AWS CLI already configured with at least PowerUser permission
* [Python 3 installed](https://www.python.org/downloads/)
* [Docker installed](https://www.docker.com/community-edition)
* [Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

## Setup process


### Create collection

```
aws rekognition create-collection --collection-id YOUR_COLLECTION_ID
```


### Create Source bucket

AWS CLI commands to package, deploy and describe outputs defined within the cloudformation stack:

```
aws s3 mb s3://YOUR_SOURCE_BUCKET_NAME

```

### Package

```bash
sam package --output-template-file packaged.yaml --s3-bucket YOUR_SOURCE_BUCKET_NAME
```

### Deploy

```
sam deploy --template-file packaged.yaml --stack-name actcast-rekognition-demo  --capabilities CAPABILITY_IAM
```


### Show Outputs

```
aws cloudformation describe-stacks --stack-name actcast-rekognition-demo --query 'Stacks[].Outputs'
```


### Show logs

```
sam logs -n actcast-rekognition-demo-RekognitionFunction-XXXXXXXXXXXXX
```
