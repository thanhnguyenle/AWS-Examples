# Create a large file

```sh
cd /workspace/AWS-Examples/s3/multipart-upload/
dd if=/dev/zero of=largefile.txt bs=1M count=50
ls -lah | grep large
```


# Create a new bucket

```sh
aws s3 mb s3://multipart-fun-abc123-3252
```

## Initiate

```sh
aws s3api create-multipart-upload --bucket multipart-fun-abc123-3252 --key 'largefile.txt'
```

> remember to grab the upload id:s3
>eg. tfKqUpJRJb4XwHGuf4zxQQTEMgR533DDyjijAn43I7sEfCGMlyzo_cnaM5GcokqZr4gbLWel_.AateLOtrFjIDDMgkUuSAO.HrObb1xFSRZURlCOjRDzdjk9iQAl9iVp

## List multipart uploads

aws s3api list-multipart-uploads --bucket multipart-fun-abc123-3252 --query Uploads[].UploadId

# Check file size
du -h largefile.txt

# Split the file
split -b 15M -d largefile.txt part-

# Check file size
ls -lh part-* | awk '{print $9, $5}'
```console
part-00 7.0M
part-01 7.0M
part-02 7.0M
part-03 7.0M
part-04 7.0M
part-05 7.0M
part-06 7.0M
part-07 1.0M
```
# Upload Part

export UPLOAD_ID="f0JFnU7zOmAdwIMIIokAYQHXrmJvKfH2CJp0G_prdW3dgE_uDAN3KM9tTr5CTgmhA3DHYEIy7kU7L9PNfe8RxuBxwFgPzjp9nbHkretJkpu7tUyEXBZJz132LBPKH1Ke"
env | grep UPLOAD

export BUCKET="multipart-fun-abc123-3252"

> This argument is of type: streaming blob. Its value must be the path to a file (e.g. path/to/file) and must not be prefixed with file:// or fileb://

aws s3api upload-part --bucket $BUCKET --key 'largefile.txt' --part-number 1 --body part-00 --upload-id $UPLOAD_ID
aws s3api upload-part --bucket $BUCKET --key 'largefile.txt' --part-number 2 --body part-01 --upload-id $UPLOAD_ID
aws s3api upload-part --bucket $BUCKET --key 'largefile.txt' --part-number 3 --body part-02 --upload-id $UPLOAD_ID
aws s3api upload-part --bucket $BUCKET --key 'largefile.txt' --part-number 4 --body part-03 --upload-id $UPLOAD_ID
aws s3api upload-part --bucket $BUCKET --key 'largefile.txt' --part-number 5 --body part-04 --upload-id $UPLOAD_ID
aws s3api upload-part --bucket $BUCKET --key 'largefile.txt' --part-number 6 --body part-05 --upload-id $UPLOAD_ID
aws s3api upload-part --bucket $BUCKET --key 'largefile.txt' --part-number 7 --body part-06 --upload-id $UPLOAD_ID

## Get all the parts with their etags

aws s3api list-parts \
  --bucket $BUCKET \
  --key 'largefile.txt' \
  --upload-id $UPLOAD_ID \
  --query "{Parts: Parts[].{PartNumber: PartNumber, ETag: ETag}}" > parts.json

## Complete

aws s3api complete-multipart-upload --multipart-upload file://parts.json --bucket $BUCKET --key 'largefile.txt' --upload-id $UPLOAD_ID

## Cleanup

aws s3 rm s3://multipart-fun-abc123-3252/largefile.txt
aws s3 rb s3://multipart-fun-abc123-3252