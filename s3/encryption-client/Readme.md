## Create a bucket

aws s3 mb s3://encrypt-client-fun-abc1-634232

# Create file key
```bash
# Generate key and save to file
openssl rand -out encrypted-file.txt 32
```

### Run our our SDK python script

```
pip install -r requirements.txt

```


# Cleanup 

aws s3 rm s3://encrypt-client-fun-abc1-634232/hello.txt
aws s3 rb s3://encrypt-client-fun-abc1-634232
