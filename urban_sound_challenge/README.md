# WifAi

## deployment instructions :

1. Create bucket : “{stage}-vonage-ml.vbc-free.com”
2. Create bucket “aws-glue-{stage}-ml-scripts.vonage.com”
   1. Add folder : /snowflake_ml/snowflake_connector/
1. upload the content of mos_prediction/libs (2 jar files ) to : s3://aws-glue-ml-scripts.vonage.com-{stage}/ml-snowflake-connector/
2. Create parameters in SSM :
   1. SF_USERNAME : ml_integration_user
   2. SF_PASSWORD : XXXX
1. Create a dynamoDB table :
   1. Name : ml-telemetry-mean-configuration
   2. Main key : configuration
   3. Set capacity configuration ( currently set on demand ) 
1. Create roles according to the definitions below  
2. Clone : https://github.com/Vonage/WifAi.git
3. (install python3 + pip)
4. Pip install -r /requirements.txt 
5. Configure env so that your default profile has access to create lambas and upload to s3 
6. Deploy lambdas :
   1. Serverless install : npm install -g serverless 
   2. In the cloned repo navigate to lambdas folder 
   3. Deployment of quality_api_model_input_generator
      1. Cd quality_api_model_input_generator
      2. npm init
      3. npm install --save serverless-python-requirements
      4. Install docker
      5. sls deploy --stage {stage} 
   1. Deployment of quality_pred_model_creation_lambda
      1. Cd quality_pred_model_creation_lambda
      2. npm init
      3. Sls deploy --stage {stage} 
   1. Deployment of quality_pred_test_no_trans
      1. Cd quality_pred_test_no_trans
      2. npm init
      3. Sls deploy --stage {stage}
1. Deploy glue scripts:
   1. Navigate to glue folder
   2. Chmod +x deploy-all.sh
   3. ./deploy-all.sh
1. Deploy step functions workflow + cloudwatch event :
   1. Go to step-functions folder
   2. Run python deploy.py





## Rules : ##
 
1.glue-quality-pred
Service : AWS glue
{
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutMetricData",
                "dynamodb:ListTables",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeVpcAttribute",
                "ec2:DescribeSecurityGroups",
                "ec2:CreateNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeVpcEndpoints",
                "ec2:DescribeSubnets",
                "ec2:DescribeRouteTables",
                "s3:ListBucket",
                "s3:GetBucketAcl",
                "s3:ListAllMyBuckets",
                "s3:GetBucketLocation",
                "ssm:GetParameters",
                "ssm:GetParameter",
                "logs:CreateLogGroup",
                "logs:PutLogEvents",
                "logs:CreateLogStream",
                "logs:AssociateKmsKey",
                "glue:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:DescribeTable",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:Query",
                "dynamodb:UpdateItem",
                "dynamodb:UpdateTable",
                "s3:CreateBucket"
            ],
            "Resource": [
                "arn:aws:s3:::aws-glue-*",
                "arn:aws:dynamodb:*:*:table/ml-telemetry-mean-configuration"
            ]
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::aws-glue-*/*",
                "arn:aws:s3:::*/*aws-glue-*/*",
                "arn:aws:s3:::*vonage-ml.vbc-free.com/*"
            ]
        },
        {
            "Sid": "VisualEditor3",
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": [
                "arn:aws:s3:::crawler-public*",
                "arn:aws:s3:::aws-glue-*",
                "arn:aws:s3:::aws-glue-*/*"
            ]
        },
        {
            "Sid": "VisualEditor4",
            "Effect": "Allow",
            "Action": "ssm:DescribeParameters",
            "Resource": "arn:aws:ssm:*:*:parameter/*"
        }
    ]
}



2.cloudwatch-events-quality-pred
Service : CloudWatch

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "states:StartExecution"
            ],
            "Resource": [
                "arn:aws:states:::stateMachine:quality-pred-step"
            ]
        }
    ]
}



3.lambda-quality-pred
Service: Lambda

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sagemaker:DescribeTrainingJob",
                "sagemaker:CreateModel",
                "sagemaker:DeleteEndpointConfig",
                "dynamodb:DeleteItem",
                "sagemaker:Search",
                "dynamodb:ListTagsOfResource",
                "s3:ListBucket",
                "sagemaker:UpdateEndpointWeightsAndCapacities",
                "s3:GetObjectAcl",
                "iam:PassRole",
                "dynamodb:DescribeTable",
                "sagemaker:DeleteEndpoint",
                "dynamodb:GetItem",
                "s3:PutObjectTagging",
                "sagemaker:DescribeEndpoint",
                "s3:DeleteObject",
                "sagemaker:InvokeEndpoint",
                "dynamodb:BatchGetItem",
                "sagemaker:CreateEndpoint",
                "dynamodb:BatchWriteItem",
                "dynamodb:ConditionCheckItem",
                "dynamodb:PutItem",
                "s3:PutMetricsConfiguration",
                "sagemaker:DescribeModel",
                "s3:PutObjectVersionTagging",
                "dynamodb:Scan",
                "sagemaker:DeleteModel",
                "dynamodb:Query",
                "dynamodb:UpdateItem",
                "sagemaker:UpdateEndpoint",
                "s3:PutObject",
                "s3:GetObject",
                "sagemaker:CreateEndpointConfig",
                "sagemaker:DescribeEndpointConfig"
            ],
            "Resource": [
                "arn:aws:sagemaker:*:*:model/quality-pred-api-ep*",
                "arn:aws:sagemaker:*:*:endpoint/*",
                "arn:aws:sagemaker:*:*:endpoint-config/quality-pred-api-ep*",
                "arn:aws:sagemaker:*:*:training-job/train-job-quality-pred",
                "arn:aws:s3:::*vonage-ml.vbc-free.com/*",
                "arn:aws:s3:::*vonage-ml.vbc-free.com",
                "arn:aws:iam:::role/vbcbe-*quality-pred-role",
                "arn:aws:dynamodb:*:*:table/ml-telemetry-mean-configuration"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "sagemaker:ListEndpointConfigs",
                "sagemaker:ListModels",
                "sagemaker:ListTrainingJobs",
                "dynamodb:DescribeLimits",
                "sagemaker:ListEndpoints"
            ],
            "Resource": "*"
        }
    ],
{
"Effect": "Allow",
"Action": [
 
               "dynamodb:DescribeTable",
               "dynamodb:GetItem",
               "dynamodb:Scan",
               "dynamodb:Query",
           ],
           "Resource": [
               "arn:aws:dynamodb:::table/ml-telemetry-mean-configuration"
           ]

}
}


4.sagemaker-quality-pred
Service: Sagemaker

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucketByTags",
                "s3:GetLifecycleConfiguration",
                "s3:GetBucketTagging",
                "s3:GetInventoryConfiguration",
                "s3:GetObjectVersionTagging",
                "s3:ListBucketVersions",
                "s3:GetBucketLogging",
                "s3:ListBucket",
                "s3:GetAccelerateConfiguration",
                "s3:GetBucketPolicy",
                "s3:GetObjectVersionTorrent",
                "s3:GetObjectAcl",
                "s3:GetEncryptionConfiguration",
                "s3:GetBucketRequestPayment",
                "s3:GetObjectVersionAcl",
                "s3:GetObjectTagging",
                "s3:GetMetricsConfiguration",
                "s3:DeleteObject",
                "s3:GetBucketPublicAccessBlock",
                "s3:GetBucketPolicyStatus",
                "s3:ListBucketMultipartUploads",
                "s3:GetBucketWebsite",
                "s3:GetBucketVersioning",
                "s3:GetBucketAcl",
                "s3:GetBucketNotification",
                "s3:GetReplicationConfiguration",
                "s3:ListMultipartUploadParts",
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetObjectTorrent",
                "s3:PutBucketLogging",
                "s3:GetBucketCORS",
                "s3:GetAnalyticsConfiguration",
                "s3:GetObjectVersionForReplication",
                "s3:GetBucketLocation",
                "s3:GetObjectVersion"
            ],
            "Resource": [
                "arn:aws:s3:::*vonage-ml.vbc-free.com/*",
                "arn:aws:s3:::*vonage-ml.vbc-free.com"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutMetricData",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
                "logs:DescribeLogStreams",
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutMetricData",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
                "logs:DescribeLogStreams",
                "s3:GetObject",
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage"
            ],
            "Resource": "*"
        }
    ]
}



5.step-function-quality-pred
Service : step-functions

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sagemaker:DescribeTrainingJob",
                "iam:PassRole",
                "lambda:InvokeFunction",
                "lambda:GetFunction",
                "sagemaker:StopTrainingJob",
                "sagemaker:CreateTrainingJob",
                "sagemaker:CreateTransformJob"
            ],
            "Resource": [
                "arn:aws:sagemaker:*:*:*quality-pred*",
                "arn:aws:lambda:*:*:function:quality-api*",
                "arn:aws:iam:::role/vbcbe-*quality-pred-role"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "events:PutEvents",
                "events:DescribeRule",
                "lambda:ListFunctions",
                "events:PutRule",
                "sagemaker:ListTrainingJobs",
                "events:TestEventPattern",
                "events:PutPermission",
                "events:DescribeEventBus",
                "events:PutTargets",
                "glue:StartJobRun",
                "glue:GetJobRun",
                "config:*",
                "events:RemovePermission",
                "glue:GetJobRuns"
            ],
            "Resource": "*"
        }
    ]
}





