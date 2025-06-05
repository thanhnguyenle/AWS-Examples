# How to Apply Temporary Credentials

## Step 1: Access AWS CloudShell and Configure CLI
Login to AWS IAM account, open CloudShell, then configure AWS CLI using your AWS access key.
**Note: Each AWS account has a limit of 2 access keys per IAM user.**

```sh
aws configure
```

## Step 2: Generate Temporary Credentials
After logging in, you can use AWS CLI to control AWS resources. Create AWS STS (Security Token Service) credentials to allow AWS CLI usage in untrusted/temporary environments:

```sh
aws sts get-session-token
```

## Step 3: Apply Temporary Credentials
Edit the file `~/.aws/credentials` or set environment variables to apply the temporary credentials for AWS CLI. 
**Note: AWS checks environment variables first, then the credentials file.**

### Option A: Environment Variables (Recommended)
```sh
export AWS_ACCESS_KEY_ID="your-temp-access-key"
export AWS_SECRET_ACCESS_KEY="your-temp-secret-key"
export AWS_SESSION_TOKEN="your-session-token"
```

### Option B: Edit Credentials File
```sh
nano ~/.aws/credentials
```

## Step 4: Verify Access
Use Security Token Service to verify temporary access permissions and confirm successful authentication:

```sh
aws sts get-caller-identity
```

This command will display your current AWS identity information, confirming that your temporary credentials are working correctly.