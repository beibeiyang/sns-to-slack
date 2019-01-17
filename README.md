# Serverless Lambda for Posting SNS Messages to Slack

This Lambda function (in both Node.js and Python):
* Deployed with the [Serverless framework](http://serverless.com/) to AWS
* Triggered by SNS
* Read SNS Notifications of any events
* Post the SNS messages to your team's Slack channel
* Support of tierred messages and show them in Green, Yellow or Red

Follow these steps to configure a webhook in Slack:

  1. Navigate to `https://<your-team>.slack.com/apps`
  2. Select "Incoming WebHooks" to install
  3. Go to the configuration page of your new service.
  4. Choose the default channel where messages will be sent and click "Add Incoming WebHooks Integration".
  5. Copy the webhook URL from the setup instructions and paste it into config file (`config.js` for Node.js and `lambda.cfg` for Python)

This Lambda must be triggered by SNS. 

The SNS message body must start with `ERROR`, `WARNING` or `SUCCESS`.

## How to Deploy Lambda Functions to AWS with Serverless and Containers

* Prerequisites:
  * Python 2.x / 3.x or Anaconda Python 2.x / 3.x
  * Python virtual environment (such as virtualenv or conda)
* Install NodeJS (included NPM): https://nodejs.org/en/
* Install Docker
* Install Serverless: `npm install -g serverless`
* Initialize NPM: `npm init`
* Install Serverless Python Requirements: `npm install --save serverless-python-requirements`
* Update config files
* Deploy Lambda:
```shell
export AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>
serverless deploy
```
* Follow this guide to package Python in Lambda with Serverless plugins:
  * https://serverless.com/blog/serverless-python-packaging/

## Reference

* Serverless.yml Reference
  * https://serverless.com/framework/docs/providers/aws/guide/serverless.yml/
* How to Handle your Python packaging in Lambda with Serverless plugins
  * https://serverless.com/blog/serverless-python-packaging/
