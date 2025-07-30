#!/usr/bin/env python3
import boto3
import sys
from botocore.exceptions import ClientError

def delete_all_objects(s3_client, bucket_name):
    """Delete all objects and versions from bucket"""
    print(f"Emptying bucket: {bucket_name}")
    
    # Delete all object versions and delete markers
    paginator = s3_client.get_paginator('list_object_versions')
    
    for page in paginator.paginate(Bucket=bucket_name):
        # Get all versions and delete markers
        objects_to_delete = []
        
        # Add all versions
        if 'Versions' in page:
            for version in page['Versions']:
                objects_to_delete.append({
                    'Key': version['Key'],
                    'VersionId': version['VersionId']
                })
        
        # Add all delete markers
        if 'DeleteMarkers' in page:
            for delete_marker in page['DeleteMarkers']:
                objects_to_delete.append({
                    'Key': delete_marker['Key'],
                    'VersionId': delete_marker['VersionId']
                })
        
        # Delete objects in batches (max 1000 per request)
        if objects_to_delete:
            for i in range(0, len(objects_to_delete), 1000):
                batch = objects_to_delete[i:i+1000]
                try:
                    response = s3_client.delete_objects(
                        Bucket=bucket_name,
                        Delete={'Objects': batch}
                    )
                    deleted_count = len(response.get('Deleted', []))
                    print(f"Deleted {deleted_count} objects/versions")
                    
                    # Check for errors
                    if 'Errors' in response:
                        for error in response['Errors']:
                            print(f"Error deleting {error['Key']}: {error['Message']}")
                            
                except ClientError as e:
                    print(f"Error during batch delete: {e}")

def delete_multipart_uploads(s3_client, bucket_name):
    """Abort all incomplete multipart uploads"""
    print(f"Aborting incomplete multipart uploads...")
    
    try:
        paginator = s3_client.get_paginator('list_multipart_uploads')
        
        for page in paginator.paginate(Bucket=bucket_name):
            if 'Uploads' in page:
                for upload in page['Uploads']:
                    try:
                        s3_client.abort_multipart_upload(
                            Bucket=bucket_name,
                            Key=upload['Key'],
                            UploadId=upload['UploadId']
                        )
                        print(f"Aborted multipart upload for: {upload['Key']}")
                    except ClientError as e:
                        print(f"Error aborting upload {upload['Key']}: {e}")
                        
    except ClientError as e:
        print(f"Error listing multipart uploads: {e}")

def force_delete_bucket(bucket_name, region=None):
    """Force delete bucket by emptying it first"""
    
    # Create S3 client
    if region:
        s3_client = boto3.client('s3', region_name=region)
    else:
        s3_client = boto3.client('s3')
    
    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Found bucket: {bucket_name}")
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"Bucket {bucket_name} does not exist")
            return
        elif error_code == '403':
            print(f"Access denied to bucket {bucket_name}")
            return
        else:
            print(f"Error accessing bucket: {e}")
            return
    
    try:
        # Step 1: Delete all objects and versions
        delete_all_objects(s3_client, bucket_name)
        
        # Step 2: Abort incomplete multipart uploads
        delete_multipart_uploads(s3_client, bucket_name)
        
        # Step 3: Delete the bucket
        print(f"Deleting bucket: {bucket_name}")
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"✅ Successfully deleted bucket: {bucket_name}")
        
    except ClientError as e:
        print(f"❌ Error deleting bucket: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 delete_bucket.py <bucket-name> [region]")
        print("Example: python3 delete_bucket.py my-bucket-name us-east-1")
        sys.exit(1)
    
    bucket_name = sys.argv[1]
    region = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Confirmation prompt
    confirm = input(f"⚠️  WARNING: This will permanently delete bucket '{bucket_name}' and ALL its contents.\nType 'DELETE' to confirm: ")
    
    if confirm != 'DELETE':
        print("Operation cancelled.")
        sys.exit(0)
    
    force_delete_bucket(bucket_name, region)

if __name__ == "__main__":
    main()