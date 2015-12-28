# Alexa-NestThermostat
Using the Alexa Skills Kit to control your Nest Thermostat

## Description
By using the Alexa Skills Kit and AWS Lambda, you can control your Nest Thermostat through your Amazon Echo.

## Usage
1. Create an Alexa Skills Kit (ASK) app, using the intent schema, custom slot values, and sample utterances in this repo. Choose an invocation name like _my Nest_.
2. Use the code in `main.py` as your Lambda function. I use [DynamoDB](https://aws.amazon.com/dynamodb/) as a simple key-value store for my Nest username and password. You can do the same, or just `self.username` and `self.password` with your own hardcoded values. Additionally, substitute `amzn1.echo-sdk-ams.app.<your-alexa-skills-id>` with the ID of the ASK skill you created. (Note: The interactions here with Nest use the Fahrenheit scale.)
4. Modify your ASK skill with the [ARN](http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) of your newly created function.
5. Test your interactions with the ASK console. When you've got it working, try it on your Echo: `Alexa, ask my Nest to turn on the heat`, or `Alexa, ask my Nest what the temperature is set to`.

## Alexa Skills Kit Documentation
The documentation for the Alexa Skills Kit is available on the [Amazon Apps and Services Developer Portal](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/).

## Resources
Here are a few direct links to Alexa and Lambda documentation:

- [Getting Started](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/getting-started-guide)
- [Invocation Name Guidelines](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/choosing-the-invocation-name-for-an-alexa-skill)
- [Developing an Alexa Skill as an AWS Lambda Function](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-lambda-function)

### Disclaimers
The code here is based off of an unsupported Nest API and is subject to change without notice. Amazon Echo does not officially support interactions with the Nest Thermostat. The authors claim no responsibility for damages to your Nest or property by use of the code within. You may incur charges using AWS Lambda. There is a free tier available for up to 1M requests per month that you may be eligible for--check [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/) for details.
