## Install Rails

```sh
gem install rails
```

## Generate a new app

```sh
rails new shogun --skip-git --skip-activerecord --api
```

https://guides.rubyonrails.org/command_line.html#rails-new

# Start App

```sh
cd shogun
bundle exec rails s
```

# Test Endpoint

```sh
curl -X POST  localhost:3000/mariko
```

# Start in production

```sh
bundle exec puma -e production -C config/puma.rb
```

# Create Bucket for Rails Artifact

```sh
aws s3 mb s3://cw-agent-app-325252


# Install These
```sh
sudo yum update -y
sudo yum install -y gcc libyaml-devel ruby-devel libxml2 libxml2-devel libxslt libxslt-devel patch redhat-rpm-config sqlite -y
gem install bundler
gem install rails
aws s3 cp s3://cw-agent-app-325252/app.zip app.zip
unzip app.zip
bundle config set --local path 'vendor/bundle'
bundle install
```

sudo chown ec2-user:ec2-user -R /usr/share/ruby3.2-gems
sudo chown ec2-user:ec2-user -R /usr/share/ruby3.2-rubygems
sudo chown ec2-user:ec2-user -R /usr/lib64/gems/ruby3.2


 # Example workflow:
      # ```yaml
      # name: Deploy to AWS
      # on:
      #   push:
      #     branches:
      #       - main
      # jobs:
      #   deploy:
      #     runs-on: ubuntu-latest
      #     steps:
      #       - name: Checkout code
      #         uses: actions/checkout@v2
      #       - name: Set up AWS CLI
      #         uses: aws-actions/configure-aws-credentials@v1
      #         with:
      #           aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
      #           aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      #           aws-region: us-west-2
      #       - name: Deploy JAR to EC2
      #         run: |
      #           aws s3 cp target/myapp.jar s3://${{ secrets.S3_BUCKET }}/myapp.jar
      #           aws ssm send-command --document-name "AWS-RunShellScript" --targets "Key=instanceids,Values=${{ secrets.EC2_INSTANCE_ID }}" --parameters 'commands=["java -jar /path/to/myapp.jar"]'
      # ```

[default]
aws_access_key_id = ASIAWPPO6QBOAFY5WFLY
aws_secret_access_key = QJv6vwEInv7pPnjqIGrJgcKPECyuxlhYknm4J8Se
aws_session_token =