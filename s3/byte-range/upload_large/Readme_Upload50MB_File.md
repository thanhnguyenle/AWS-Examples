## Create a bucket

aws s3 mb s3://range-run-large-abc123-53252

# Create a large file

```sh
cd s3/byte-range/upload_large
dd if=/dev/zero of=largefile.txt bs=1M count=50
ls -lah | grep large | awk '{print $9, $5}'
```

## Upload our file

aws s3api put-object --bucket range-run-large-abc123-53252 --key largefile.txt --body largefile.txt

## Download file by fetch byte range
python download_largefile_byrange.py 

## Check file same content with file already uploaded
1. Get object head of file at s3
aws s3api head-object --bucket range-run-large-abc123-53252 --key largefile.txt

<!-- {
    "AcceptRanges": "bytes",
    "LastModified": "2025-07-25T09:41:21+00:00",
    "ContentLength": 52428800,
    "ETag": "\"25e317773f308e446cc84c503a6d1f85\"",
    "ContentType": "binary/octet-stream",
    "ServerSideEncryption": "AES256",
    "Metadata": {}
} -->

2. Check content of largedownloaded.txt file encoded to md5
md5sum largedownloaded.txt
<!-- 
25e317773f308e446cc84c503a6d1f85 
=> match with etag => content not change => origin file
-->

3. Etag can different because method upload (multipart or not) => Check by checksum
aws s3api get-object-attributes --bucket range-run-large-abc123-53252 --key largefile.txt --object-attributes Checksum
<!-- 
    {
        "LastModified": "2025-07-25T09:41:21+00:00",
        "Checksum": {
            "ChecksumCRC64NVME": "ZfX5vT9m/o8=",
            "ChecksumType": "FULL_OBJECT"
    }
} -->

python3 -c "import base64,awscrt.checksums; data=open('largedownloaded.txt','rb').read(); print(base64.b64encode(awscrt.checksums.crc64nvme(data).to_bytes(8,'big')).decode())"
<!-- 
ZfX5vT9m/o8=
=> ORIGIN FILE
 -->