## Create a bucket

```bash
aws s3 mb s3://encryption-fun-ab123-13567
```

### Create a file and Put Object with encrpytion SS3-S3

```bash
echo "Hello World" > hello.txt
aws s3 cp hello.txt  s3://encryption-fun-ab123-13567
```
### Put Object with encryption of SS3-KMS

```bash
aws s3api put-object \
--bucket encryption-fun-ab123-13567 \
--key hello.txt \
--body hello.txt \
--server-side-encryption "aws:kms" \
--ssekms-key-id "7fbd6354-cfe6-4a4f-9ebf-d5a7e33536ce"
```
### Put Object with SSE-C [Failed Attempt]
```bash
export BASE64_ENCODED_KEY=$(openssl rand -base64 32)
echo  $BASE64_ENCODED_KEY

export MD5_VALUE=$(echo $BASE64_ENCODED_KEY | md5sum | awk '{print $1}' | base64 -w0)
echo  $MD5_VALUE

aws s3api put-object \
--bucket encryption-fun-ab123-13567 \
--key hello.txt \
--body hello.txt \
--sse-customer-algorithm AES256 \
--sse-customer-key $BASE64_ENCODED_KEY \
--sse-customer-key-md5 $MD5_VALUE
```

An error occurred (InvalidArgument) when calling the PutObject operation: The calculated MD5 hash of the key did not match the hash that was provided.

#### What Was Wrong:
##### Your process:

- Generate 32 random bytes → base64 encode → $BASE64_ENCODED_KEY
- Take base64 string → MD5 hash → base64 encode again ❌

##### Correct process:

- Generate 32 random bytes
- Base64 encode for the key parameter
- MD5 hash the original raw bytes → base64 encode the hash

#### Why This Matters:
##### AWS expects:
```
--sse-customer-key: Base64-encoded 256-bit key
--sse-customer-key-md5: Base64-encoded MD5 hash of the raw key bytes
```
The MD5 is used by AWS to verify the key wasn't corrupted during transmission.

### Put Object with SSE-C via aws s3

https://catalog.us-east-1.prod.workshops.aws/workshops/aad9ff1e-b607-45bc-893f-121ea5224f24/en-US/s3/serverside/ssec


```bash
openssl rand -out ssec.key 32

aws s3 cp hello.txt s3://encryption-fun-ab123-13567/hello.txt \
--sse-c AES256 \
--sse-c-key fileb://ssec.key

aws s3 cp s3://encryption-fun-ab123-13567/hello.txt hello.txt --sse-c AES256 --sse-c-key fileb://ssec.key
```

# View object metadata
```bash
aws s3api head-object \
--bucket encryption-fun-ab123-13567 \
--key hello.txt \
--sse-customer-algorithm AES256 \
--sse-customer-key fileb://ssec.key
```

# List objects with metadata
```bash
aws s3api list-objects-v2 \
--bucket encryption-fun-ab123-13567
```

# Download object
```bash
aws s3 cp s3://encryption-fun-ab123-13567/hello.txt . \
--sse-c AES256 \
--sse-c-key fileb://ssec.key
```