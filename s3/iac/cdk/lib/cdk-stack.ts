import { Stack, StackProps } from 'aws-cdk-lib';
import { Bucket } from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export class CdkStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Create an S3 bucket
    const bucket = new Bucket(this, 'MyBucket', {
      // Optional: Add bucket configuration
      // bucketName: 'my-unique-bucket-name',
      // versioned: true,
      // encryption: BucketEncryption.S3_MANAGED,
      // blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      // removalPolicy: RemovalPolicy.DESTROY, // Use with caution in production
    });

    // Optional: Output the bucket name
    // new CfnOutput(this, 'BucketName', {
    //   value: bucket.bucketName,
    //   description: 'Name of the S3 bucket',
    // });
  }
}