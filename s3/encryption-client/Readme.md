## Create a bucket

aws s3 mb s3://encrypt-client-fun-abc1-634232


### Run our our SDK python script

```bash
pip install -r requirements.txt

python encryption_client.py
```


# Cleanup 

```bash
aws s3 rm s3://encrypt-client-fun-abc1-634232/hello.txt
aws s3 rb s3://encrypt-client-fun-abc1-634232
```
