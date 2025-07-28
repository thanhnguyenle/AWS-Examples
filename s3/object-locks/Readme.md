## Create a new folder

```sh
aws s3 mb s3://object-lock-my-testing-1209
```

## Turn on S3 Versioning

aws s3api put-bucket-versioning --bucket object-lock-my-testing-1209 --versioning-configuration Status=Enabled

## Turn on Object Locking (GOVERNANCE MODE - FLEXIBITY)

aws s3api put-object-lock-configuration \
    --bucket object-lock-my-testing-1209\
    --object-lock-configuration '{ "ObjectLockEnabled": "Enabled", "Rule": { "DefaultRetention": { "Mode": "GOVERNANCE", "Days": 1 }}}'

## New file and upload

echo "This is the gov2" > gov.txt
aws s3 cp gov.txt s3://object-lock-my-testing-1209

## delete the file (It can delete file because this account is owner of this file)

aws s3 rm s3://object-lock-my-testing-1209/gov.txt

## delete the versioned file (if provided version-id of object and with --bypass-governance-retention, i can delete object present for this version ID)

aws s3api delete-object --bucket="object-lock-my-testing-1209" --key "gov.txt" --version-id="knWY1X1JxuR_h8Uk_z4ajeso7Gqjvqm6" --bypass-governance-retention 

## use compliance mode for s3 object

aws s3api put-object --bucket="object-lock-my-testing-1209" --key "gov.txt" --body="compliance.txt" --object-lock-mode COMPLIANCE --object-lock-retain-until-date="2025-07-20T18:00:00Z"

## try and delete specific version (Try use --bypass-governance-retention it still cannot delete)

aws s3api delete-object --bucket="object-lock-my-testing-1209" --key "gov.txt" --version-id="Lma20PN9c19QkjUAB4zXaN_BGQI3HO9t" --bypass-compliance-retention

### Legal Holds

touch legal.txt

aws s3 cp legal.txt s3://object-lock-my-testing-1209/legal.txt

aws s3api put-object-legal-hold --bucket "object-lock-my-testing-1209" --key "legal.txt" --legal-hold Status=ON

aws s3 rm s3://object-lock-my-testing-1209/legal.txt

aws s3api list-object-versions --bucket  object-lock-my-testing-1209

aws s3api delete-object --bucket="object-lock-my-testing-1209" --key "legal.txt" --version-id="limcmf.jxcW.z__vZELviwr3_vvQzK5p"


aws s3api put-object-legal-hold --bucket "object-lock-my-testing-1209" --version-id="limcmf.jxcW.z__vZELviwr3_vvQzK5p" --key "legal.txt" --legal-hold Status=OFF

aws s3api delete-object --bucket="object-lock-my-testing-1209" --key "legal.txt" --version-id="limcmf.jxcW.z__vZELviwr3_vvQzK5p"

aws s3api delete-object --bucket="object-lock-my-testing-1209" --key "legal.txt" --version-id="KTD_YBuWo.MeXUoS4r51CaGZ5c7wsiOY" --bypass-governance-retention 



aws s3api delete-object \
  --bucket object-lock-my-testing-1209 \
  --key gov.txt \
  --version-id plLmCUUPe5B00WlkUmiUGXl0ME_.OQnp