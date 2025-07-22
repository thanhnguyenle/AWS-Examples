#!/usr/bin/env python3
"""
S3 Client-Side Encryption Example
Encrypts data before uploading to S3 and demonstrates decryption on download
"""

import boto3
import base64
from botocore.client import Config
from botocore.exceptions import ClientError, NoCredentialsError
from cryptography.fernet import Fernet

def main():
    # Configuration
    BUCKET_NAME = 'encrypt-client-fun-abc1-634232'  # Replace with your actual bucket name
    FILE_KEY = 'encrypted-file.txt'
    REGION = 'us-east-1'  # Replace with your region
    
    try:
        # Initialize S3 client
        s3 = boto3.client('s3', 
            region_name=REGION,
            config=Config(
                s3={'addressing_style': 'path'}
            )
        )
        
        # Test S3 connectivity
        print("Testing S3 connectivity...")
        s3.list_buckets()
        print("✓ S3 connection successful")
        
        # Check if bucket exists
        try:
            s3.head_bucket(Bucket=BUCKET_NAME)
            print(f"✓ Bucket '{BUCKET_NAME}' exists and is accessible")
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                print(f"❌ Bucket '{BUCKET_NAME}' does not exist")
                print("Please create the bucket first or update BUCKET_NAME variable")
                return
            else:
                print(f"❌ Error accessing bucket: {e}")
                return
        
        # Generate encryption key
        print("\n🔐 Generating encryption key...")
        
        # What is Fernet? # Fernet is a symmetric encryption method that uses a key to encrypt and decrypt data.
        # It ensures that the data can only be decrypted by someone who has the key.
        # Generate a new key for encryption
        # Note: In production, you should use a secure key management system (KMS, HSM, etc.) to manage your keys.
        key = Fernet.generate_key()
        cipher = Fernet(key)
        
        # Display key (in production, store this securely!)
        key_b64 = base64.b64encode(key).decode('utf-8')
        print(f"Encryption key (base64): {key_b64}")
        print("⚠️  IMPORTANT: Save this key securely! You'll need it to decrypt the data.")
        
        # Data to encrypt
        original_data = b"This is sensitive data that will be encrypted before upload to S3!"
        print(f"\n📝 Original data: {original_data.decode('utf-8')}")
        
        # Encrypt data client-side
        print("\n🔒 Encrypting data...")
        encrypted_data = cipher.encrypt(original_data)
        print(f"Encrypted data length: {len(encrypted_data)} bytes")
        
        # Upload encrypted data to S3
        print(f"\n☁️  Uploading encrypted data to s3://{BUCKET_NAME}/{FILE_KEY}")
        s3.put_object(
            Bucket=BUCKET_NAME, 
            Key=FILE_KEY, 
            Body=encrypted_data,
            Metadata={
                'encryption': 'client-side-fernet',
                'original-size': str(len(original_data))
            }
        )
        print("✓ Upload successful!")
        
        # Download and decrypt data
        print(f"\n⬇️  Downloading encrypted data from S3...")
        response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
        downloaded_encrypted_data = response['Body'].read()
        
        print(f"Downloaded {len(downloaded_encrypted_data)} bytes")
        print(f"Metadata: {response.get('Metadata', {})}")
        
        # Decrypt the downloaded data
        print("\n🔓 Decrypting downloaded data...")
        decrypted_data = cipher.decrypt(downloaded_encrypted_data)
        print(f"Decrypted data: {decrypted_data.decode('utf-8')}")
        
        # Verify data integrity
        if decrypted_data == original_data:
            print("✅ SUCCESS: Data integrity verified! Original and decrypted data match.")
        else:
            print("❌ ERROR: Data integrity check failed!")
        
        # Save key to file (optional)
        save_key = input("\n💾 Save encryption key to file? (y/N): ").lower().strip()
        if save_key == 'y':
            with open('encryption_key.txt', 'w') as f:
                f.write(key_b64)
            print("✓ Encryption key saved to 'encryption_key.txt'")
            print("⚠️  Keep this file secure and never commit it to version control!")
        
        print("\n🎉 Client-side encryption demo completed successfully!")
        
    except NoCredentialsError:
        print("❌ AWS credentials not found!")
        print("Please configure AWS credentials using:")
        print("1. AWS CLI: aws configure")
        print("2. Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
        print("3. IAM roles (if running on EC2)")
        
    except ClientError as e:
        print(f"❌ AWS Error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def load_key_and_decrypt_file(bucket_name, file_key, encryption_key_b64):
    """
    Helper function to decrypt a file using a saved key
    """
    try:
        # Decode the key
        key = base64.b64decode(encryption_key_b64.encode('utf-8'))
        cipher = Fernet(key)
        
        # Initialize S3 client
        s3 = boto3.client('s3')
        
        # Download and decrypt
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        encrypted_data = response['Body'].read()
        decrypted_data = cipher.decrypt(encrypted_data)
        
        return decrypted_data.decode('utf-8')
        
    except Exception as e:
        print(f"Error decrypting file: {e}")
        return None

if __name__ == "__main__":
    print("🚀 S3 Client-Side Encryption Demo")
    print("=" * 50)
    main()
    
    print("\n" + "=" * 50)
    print("📚 USAGE NOTES:")
    print("1. Update BUCKET_NAME variable with your actual S3 bucket")
    print("2. Ensure AWS credentials are configured")
    print("3. Save the encryption key securely - you need it to decrypt!")
    print("4. In production, use proper key management (AWS KMS, HSM, etc.)")