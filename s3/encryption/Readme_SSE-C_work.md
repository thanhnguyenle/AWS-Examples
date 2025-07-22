# Method 1: Generate key and hash correctly
```bash
export BASE64_ENCODED_KEY=$(openssl rand -base64 32)
echo "Key: $BASE64_ENCODED_KEY"
```

# Correct: Hash the raw key bytes, not the base64 string
```bash
export MD5_VALUE=$(echo $BASE64_ENCODED_KEY | base64 -d | md5sum | awk '{print $1}' | xxd -r -p | base64 -w0)
echo "MD5: $MD5_VALUE"
```

```bash
aws s3api put-object \
--bucket encryption-fun-ab123-13567 \
--key hello.txt \
--body hello.txt \
--sse-customer-algorithm AES256 \
--sse-customer-key $BASE64_ENCODED_KEY \
--sse-customer-key-md5 $MD5_VALUE
```

# Method 2: Alternative approach (simpler)
# Generate raw key, then encode both key and MD5
```bash
RANDOM_KEY=$(openssl rand 32)
export BASE64_ENCODED_KEY=$(echo -n "$RANDOM_KEY" | base64 -w0)
export MD5_VALUE=$(echo -n "$RANDOM_KEY" | md5sum | awk '{print $1}' | xxd -r -p | base64 -w0)

echo "Key: $BASE64_ENCODED_KEY"
echo "MD5: $MD5_VALUE"

aws s3api put-object \
--bucket encryption-fun-ab123-13567 \
--key hello.txt \
--body hello.txt \
--sse-customer-algorithm AES256 \
--sse-customer-key $BASE64_ENCODED_KEY \
--sse-customer-key-md5 $MD5_VALUE
```

# Method 3: Most reliable approach
```bash
# Create temporary files to avoid shell quirks
openssl rand 32 > /tmp/key.bin
export BASE64_ENCODED_KEY=$(base64 -w0 < /tmp/key.bin)
export MD5_VALUE=$(md5sum /tmp/key.bin | awk '{print $1}' | xxd -r -p | base64 -w0)

echo "Key: $BASE64_ENCODED_KEY"
echo "MD5: $MD5_VALUE"

aws s3api put-object \
--bucket encryption-fun-ab123-13567 \
--key hello.txt \
--body hello.txt \
--sse-customer-algorithm AES256 \
--sse-customer-key $BASE64_ENCODED_KEY \
--sse-customer-key-md5 $MD5_VALUE
```

# Clean up
```bash
rm -f /tmp/key.bin
```