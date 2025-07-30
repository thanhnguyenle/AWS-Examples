# Elastic Beanstalk Deployment Testing Guide

## 1. Prerequisites Setup

### Deploy CloudFormation Stack

Before updating the template, let's get the actual available platforms in your region:
```bash
# Get the latest supported Node.js solution stack (simpler approach)
aws elasticbeanstalk list-available-solution-stacks \
  --region us-east-1 \
  --query 'SolutionStacks[?contains(@, `Node.js`)] | [0]' \
  --output text
```

```bash
# Deploy the infrastructure
aws cloudformation create-stack \
  --stack-name eb-test-stack \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1 \
  --parameters \
    ParameterKey=ApplicationName,ParameterValue=test-app \
    ParameterKey=VpcId,ParameterValue=vpc-02b92c6da0a9510cf \
    ParameterKey=SubnetIds,ParameterValue=subnet-0ae1c6149542760b4\\,subnet-0cd38379ead627d09

# Wait for completion
aws cloudformation wait stack-create-complete --stack-name eb-test-stack
```

## 2. Prepare Application

### Create Application Files And upload to S3
```bash
cd elastic-beanstalk/app/

# Create application zip
zip -r app-v1.zip app.js package.json

# Create bucket
aws s3 mb s3://my-bucket-eb-28958432

# Upload the template to the S3 bucket
aws s3 cp app-v1.zip s3://my-bucket-eb-28958432
```

## 3. Manual Deployment Strategy Testing

### Get Environment Information
```bash
# Get environment name from CloudFormation output
ENV_NAME=$(aws cloudformation describe-stacks \
  --stack-name eb-test-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`EnvironmentName`].OutputValue' \
  --output text)

APP_NAME=$(aws cloudformation describe-stacks \
  --stack-name eb-test-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`ApplicationName`].OutputValue' \
  --output text)

echo "Environment: $ENV_NAME"
echo "Application: $APP_NAME"
```

## 4. Test Different Deployment Strategies

### A. Rolling Deployment
```bash
# Set to Rolling deployment
aws elasticbeanstalk update-environment \
  --environment-name $ENV_NAME \
  --option-settings \
    Namespace=aws:elasticbeanstalk:command,OptionName=DeploymentPolicy,Value=Rolling \
    Namespace=aws:elasticbeanstalk:command,OptionName=BatchSizeType,Value=Fixed \
    Namespace=aws:elasticbeanstalk:command,OptionName=BatchSize,Value=1 \
    Namespace=aws:elasticbeanstalk:application:environment,OptionName=APP_VERSION,Value=v1.0-rolling \
    Namespace=aws:elasticbeanstalk:application:environment,OptionName=DEPLOYMENT_STRATEGY,Value=Rolling

# Create new version and deploy
aws elasticbeanstalk create-application-version \
  --application-name $APP_NAME \
  --version-label v1.0-rolling \
  --source-bundle S3Bucket=my-bucket-eb-28958432,S3Key=app-v1.zip

aws elasticbeanstalk update-environment \
  --environment-name $ENV_NAME \
  --version-label v1.0-rolling

echo "Rolling deployment initiated. Monitor with:"
echo "aws elasticbeanstalk describe-environment-health --environment-name $ENV_NAME --attribute-names All"
```

### B. Immutable Deployment
```bash
# Set to Immutable deployment
aws elasticbeanstalk update-environment \
  --environment-name $ENV_NAME \
  --option-settings \
    Namespace=aws:elasticbeanstalk:command,OptionName=DeploymentPolicy,Value=Immutable \
    Namespace=aws:elasticbeanstalk:application:environment,OptionName=APP_VERSION,Value=v1.0-immutable \
    Namespace=aws:elasticbeanstalk:application:environment,OptionName=DEPLOYMENT_STRATEGY,Value=Immutable

# Wait for environment to be ready
aws elasticbeanstalk wait environment-updated --environment-name $ENV_NAME

# Deploy new version
aws elasticbeanstalk create-application-version \
  --application-name $APP_NAME \
  --version-label v1.0-immutable \
  --source-bundle S3Bucket=my-bucket-eb-28958432,S3Key=app-v1.zip

aws elasticbeanstalk update-environment \
  --environment-name $ENV_NAME \
  --version-label v1.0-immutable

echo "Immutable deployment initiated."
```

### C. Blue/Green Deployment (Manual Setup)
```bash
# Create a second environment for Blue/Green
aws elasticbeanstalk create-environment \
  --application-name $APP_NAME \
  --environment-name ${ENV_NAME}-blue \
  --solution-stack-name "64bit Amazon Linux 2023 v6.6.1 running Node.js 20" \
  --option-settings \
    Namespace=aws:autoscaling:launchconfiguration,OptionName=InstanceType,Value=t2.micro \
    Namespace=aws:elasticbeanstalk:environment,OptionName=EnvironmentType,Value=SingleInstance \
    Namespace=aws:elasticbeanstalk:application:environment,OptionName=APP_VERSION,Value=v1.0-blue \
    Namespace=aws:elasticbeanstalk:application:environment,OptionName=DEPLOYMENT_STRATEGY,Value=Blue-Green

# Wait for blue environment to be ready
aws elasticbeanstalk wait environment-updated --environment-name ${ENV_NAME}-blue

# Get both environment URLs
GREEN_URL=$(aws elasticbeanstalk describe-environments \
  --environment-names $ENV_NAME \
  --query 'Environments[0].EndpointURL' --output text)

BLUE_URL=$(aws elasticbeanstalk describe-environments \
  --environment-names ${ENV_NAME}-blue \
  --query 'Environments[0].EndpointURL' --output text)

echo "Green Environment: http://$GREEN_URL"
echo "Blue Environment: http://$BLUE_URL"

# To swap environments (Blue/Green switch)
echo "To perform Blue/Green swap:"
echo "aws elasticbeanstalk swap-environment-cnames \\"
echo "  --source-environment-name $ENV_NAME \\"
echo "  --destination-environment-name ${ENV_NAME}-blue"
```

## 5. Deploy Your Custom Application

### Upload Custom App Version
```bash
# First, upload your zip to S3
S3_BUCKET=$(aws cloudformation describe-stacks \
  --stack-name eb-test-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`S3Bucket`].OutputValue' \
  --output text)

aws s3 cp app-v1.zip s3://$S3_BUCKET/

# Create application version from your custom app
aws elasticbeanstalk create-application-version \
  --application-name $APP_NAME \
  --version-label my-app-v1.0 \
  --source-bundle S3Bucket=$S3_BUCKET,S3Key=app-v1.zip

# Deploy your custom app
aws elasticbeanstalk update-environment \
  --environment-name $ENV_NAME \
  --version-label my-app-v1.0
```

## 6. Create Different Versions for Testing

### Create Version 2 with Changes
```bash
# Modify app.js to change VERSION to 'v2.0'
sed -i 's/v1.0/v2.0/g' app.js
zip -r app-v2.zip app.js package.json

# Upload and deploy v2
aws s3 cp app-v2.zip s3://$S3_BUCKET/
aws elasticbeanstalk create-application-version \
  --application-name $APP_NAME \
  --version-label my-app-v2.0 \
  --source-bundle S3Bucket=$S3_BUCKET,S3Key=app-v2.zip

# Deploy with different strategy
aws elasticbeanstalk update-environment \
  --environment-name $ENV_NAME \
  --version-label my-app-v2.0
```

## 7. Monitoring Commands

### Check Deployment Status
```bash
# Environment status
aws elasticbeanstalk describe-environments --environment-names $ENV_NAME

# Environment health
aws elasticbeanstalk describe-environment-health \
  --environment-name $ENV_NAME \
  --attribute-names All

# Recent events
aws elasticbeanstalk describe-events \
  --environment-name $ENV_NAME \
  --max-items 10

# Application versions
aws elasticbeanstalk describe-application-versions \
  --application-name $APP_NAME
```

### Test the Application
```bash
# Get environment URL
APP_URL=$(aws elasticbeanstalk describe-environments \
  --environment-names $ENV_NAME \
  --query 'Environments[0].EndpointURL' --output text)

# Test endpoints
curl http://$APP_URL/
curl http://$APP_URL/health
curl http://$APP_URL/version
```

## 8. Cleanup
```bash
# Terminate environments
aws elasticbeanstalk terminate-environment --environment-name $ENV_NAME
aws elasticbeanstalk terminate-environment --environment-name ${ENV_NAME}-blue

# Delete CloudFormation stack (after environments are terminated)
aws cloudformation delete-stack --stack-name eb-test-stack
```

## Quick Test Script
```bash
#!/bin/bash
# quick-test.sh - Run different deployment strategies

ENV_NAME="your-env-name"
APP_NAME="your-app-name"

strategies=("Rolling" "Immutable")

for strategy in "${strategies[@]}"; do
  echo "Testing $strategy deployment..."
  
  aws elasticbeanstalk update-environment \
    --environment-name $ENV_NAME \
    --option-settings \
      Namespace=aws:elasticbeanstalk:command,OptionName=DeploymentPolicy,Value=$strategy \
      Namespace=aws:elasticbeanstalk:application:environment,OptionName=DEPLOYMENT_STRATEGY,Value=$strategy
  
  aws elasticbeanstalk wait environment-updated --environment-name $ENV_NAME
  echo "$strategy deployment complete"
  sleep 30
done
```

This guide provides a complete testing framework for all Elastic Beanstalk deployment strategies on AWS Free Tier!