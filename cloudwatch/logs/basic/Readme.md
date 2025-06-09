## Create Logging Data

```sh
NENTRIES=10 python generate_logs.py > web_server_logs.log
```


## Create Log Group

```sh
aws logs create-log-group --log-group-name "/example/basic/app2"
```


## Set Retention on Log Group

```sh
aws logs put-retention-policy --log-group-name "/example/basic/app2" --retention-in-days 1
```


## Create Log Stream

```sh
aws logs create-log-stream --log-group-name "/example/basic/app2" --log-stream-name $(date +%s)
```

# List all logs streams in a log group in AWS
```sh
aws logs describe-log-streams --log-group-name "/example/basic/app2"
```

## Send Logs to Log Stream
```sh
aws logs put-log-events --log-group-name my-logs --log-stream-name 20150601 --log-events file://events
```
# Delete log group

```sh
aws logs delete-log-group --log-group-name "/example/basic/app2"
```

## Ruby SDK Logs

```sh
bundle install
bundle exec rake log
```