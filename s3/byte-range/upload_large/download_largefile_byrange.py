import boto3

def download_large_file_by_ranges(bucket, key, chunk_size_mb=8):
    s3 = boto3.client('s3')
    
    # Get file size first
    response = s3.head_object(Bucket=bucket, Key=key)
    file_size = response['ContentLength']  # Total bytes
    
    chunk_size = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    parts = []
    
    # Generate ranges automatically
    for start in range(0, file_size, chunk_size):
        end = min(start + chunk_size - 1, file_size - 1)
        byte_range = f'bytes={start}-{end}'
        
        print(f"Downloading {byte_range}")
        response = s3.get_object(Bucket=bucket, Key=key, Range=byte_range)
        parts.append(response['Body'].read())
    
    # Reassemble file
    complete_file = b''.join(parts)
    return complete_file

file_data = download_large_file_by_ranges("range-run-large-abc123-53252", "largefile.txt")

with open("largedownloaded.txt", 'wb') as f:
        f.write(file_data)