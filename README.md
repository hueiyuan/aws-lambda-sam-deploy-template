# aws-lambda-sam-deploy-template
the repo includes my experience which use sam to deploy aws lambda function. If need it, we have to replace value for our real situation.

## How to use SAM?
1. You need to install sam cli on localhost.
* MacOS (Use homebrew)
```
brew tap aws/tap
brew install aws-sam-cli
sam --version
```
* linux (Ubuntu)
```
wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip
sudo ./sam-installation/install
sam --version
```

2. Prepare related file for deploy
* `samconfig.toml`: sam related configuration file.
* `template.yaml`: lambda function cloudformation yaml, sam will deploy this to cf as stack.
* `src/`: it is stored lambda function related script and requirements.txt
* `event/`: it emulates event trigger.

3. build your application as container
```
sam build --use-container
```
You need to use `--use-container` to install additional python lib. Since some libs are not support on aws lambda.

4. deploy your lambda function.
```
sam deploy --guided
```
