# Create Bucket for Nested Stack Templates
aws s3 mb s3://my-nested-stack-templates-123487043

# Upload the template to the S3 bucket
aws s3 cp s3_bucket.template s3://my-nested-stack-templates-123487043

# Full public access (dont need set - BECAUSE Cloudformation built-in cross-service permissions)
aws s3api put-public-access-block \
    --bucket my-nested-stack-templates-123487043 \
    --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Update bucket policy to allow CloudFormation to access the templates (dont need set - BECAUSE Cloudformation built-in cross-service permissions)
aws s3api put-bucket-policy \
  --bucket my-nested-stack-templates-123487043 \
  --policy file://bucket-policy-template.json
