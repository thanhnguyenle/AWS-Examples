## Create a new bucket

```sh
aws s3api create-bucket --bucket acl-example-abc-523590 --region us-east-1
```

## Turn of Block Public Access for ACLs

```sh
aws s3api put-public-access-block \
--bucket acl-example-abc-523590 \
--public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

```sh
aws s3api get-public-access-block --bucket acl-example-abc-523590
```

## Change Bucket Ownership


```sh
aws s3api put-bucket-ownership-controls \
--bucket acl-example-abc-523590 \
--ownership-controls="Rules=[{ObjectOwnership=BucketOwnerPreferred}]"
```

## Change ACLs to allow for a user in another AWS Account

```sh
aws s3api put-bucket-acl \
--bucket acl-example-abc-523590 \
--access-control-policy file://policy.json
```

## Access Bucket from other account

```sh
touch bootcamp.txt
aws s3 cp bootcamp.txt s3://acl-example-abc-523590
aws s3 ls s3://acl-example-abc-523590
```

## Cleanup

```sh
aws s3 rm s3://acl-example-abc-523590/bootcamp.txt
aws s3 rb s3://acl-example-abc-523590
```