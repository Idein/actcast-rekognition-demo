# Face Recognition with Actcast and Amazon Rekognition

This is a sample code to build a practical face recognition system combining [Actcast](https://actcast.io) and [Amazon Rekognition](https://aws.amazon.com/rekognition/).

Using Amazon Rekognition's API, you can easily build a face recognition system.
However, when analyzing real-world images captured by security cameras, etc., it is necessary to process a large number of images captured continuously, which incurs high network traffic costs and API usage fees.
Therefore, **an edge-cloud hybrid architecture** is required, where the first stage is analyzed on the edge and the second stage only when necessary on the cloud.

In this sample project, we use Raspberry Pi to detect and track faces on the edge, and calls Rekognition API only when it detects a person's face to turn it into a Face ID.

# Setup

1. Setup the AWS side software
2. Setup Raspberry Pi and face detection app
3. Connect them using Actcastg's Cast function

## Setup the AWS side software

Below is a brief explanation of what we have generated for you:

```bash
.
├── README.md                   <-- This instructions file
├── func                        <-- Source code for a lambda function
│   ├── __init__.py
│   ├── app.py                  <-- Lambda function code
│   └── requirements.txt        <-- Python dependencies
└── template.yaml               <-- SAM Template
```

Requirements.

* [AWS CLI](https://aws.amazon.com/cli/) configured with at least PowerUser permission
* [AWS SAM CLI](https://aws.amazon.com/serverless/sam/)


First of all, create a collection to store face features.

```
aws rekognition create-collection --collection-id YOUR_COLLECTION_ID
```

Then package the software and deploy them.

```
aws s3 mb s3://your-source-bucket-name
sam package --output-template-file packaged.yaml --s3-bucket your-source-bucket-name
sam deploy --template-file packaged.yaml --stack-name your-stack-name  --capabilities CAPABILITY_IAM
```

After the deployment is sucessfully completed, run the following command to check the API endpoint and other resources.

```
aws cloudformation describe-stacks --stack-name your-stack-name --query 'Stacks[].Outputs'
```

## Setup Raspberry Pi and face detection app

Setup a Raspberry Pi following [Actcast's Tutorial](https://actcast.io/docs/) and install **Face Tracking** App.

## Setup Cast

Set webhook endpoint, shown in the output of `describe-stacks` command,  and JSON template to the app's Cast setting like this.

```
{
"image": "{{ data.face }}"
}
```
