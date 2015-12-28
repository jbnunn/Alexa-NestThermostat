# Alexa-NestThermostat

## Description
Use your Amazon Echo and the Alexa Skills Kit to control your Nest Thermostat. You'll create an Alexa Skills Kit (ASK) app that fires off requests to AWS Lambda. Lambda in turn will call the NEST API to control a thermostat in your structure.

## Usage
1. Create an Alexa Skills Kit (ASK) app, using the intent schema, custom slot values, and sample utterances in this repo. Choose an invocation name like _my Nest_.
2. Use the code in `main.py` as your Lambda function. I use [DynamoDB](https://aws.amazon.com/dynamodb/) as a simple key-value store for my Nest username and password. You can do the same, or just `self.username` and `self.password` with your own hardcoded values. Additionally, substitute `amzn1.echo-sdk-ams.app.<your-alexa-skills-id>` with the ID of the ASK skill you created.
4. Modify your ASK skill with the [ARN](http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) of your newly created function.
5. Test your interactions with the ASK console. When you've got it working, try it on your Echo: `Alexa, ask my Nest to turn on the heat`, or `Alexa, ask my Nest what the temperature is set to`.

## Caveats
- The Nest by default uses the Celsius temperature scale. This code does conversion to use Fahrenheit. If you wish to use Celsius, look at the functions `temp_in` and `temp_out`, which do the conversions.
- If you have more than one Nest Thermostat in your structure, you'll have to specify the index of the one you want to control. This code defaults to the first unit found when it queries your available thermostats (`index=0`).


## Alexa Skills Kit Documentation
The documentation for the Alexa Skills Kit is available on the [Amazon Apps and Services Developer Portal](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/).

## Resources
Here are a few direct links to Alexa and Lambda documentation:

- [Getting Started](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/getting-started-guide)
- [Invocation Name Guidelines](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/choosing-the-invocation-name-for-an-alexa-skill)
- [Developing an Alexa Skill as an AWS Lambda Function](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-lambda-function)


## Disclaimers
The code here is based off of an unsupported Nest API and is subject to change without notice. Amazon Echo does not officially support interactions with the Nest Thermostat. The authors claim no responsibility for damages to your Nest or property by use of the code within. You may incur charges using AWS Lambda, but there is a free tier available for up to 1M requests per month that you may be eligible for--check [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/) for details.

## License
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
