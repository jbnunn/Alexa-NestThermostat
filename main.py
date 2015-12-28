# December 2015, Jeff Nunn
# @jbnunn
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>

import boto3
import json
import urllib
import urllib2

def lambda_handler(event, context):

    if event['session']['application']['applicationId'] != "amzn1.echo-sdk-ams.app.<your-alexa-skills-id>":
        print "Invalid Application ID"
    else:
        sessionAttributes = {}

        # Grab app credentials from our DynamoDB keystore
        dynamodb    = boto3.resource('dynamodb')
        table       = dynamodb.Table('env')
        response    = table.get_item(Key={'key': 'NEST'})
        username    = response['Item']['env']['email']
        password    = response['Item']['env']['password']

        nest = Nest(username, password)
        nest.login()

        if event['session']['new']:
            onSessionStarted(event['request']['requestId'], event['session'])
        if event['request']['type'] == "LaunchRequest":
            speechlet = onLaunch(event['request'], event['session'])
            response = buildResponse(sessionAttributes, speechlet)
        elif event['request']['type'] == "IntentRequest":
            speechlet = onIntent(event['request'], event['session'], nest)
            response = buildResponse(sessionAttributes, speechlet)
        elif event['request']['type'] == "SessionEndedRequest":
            speechlet = onSessionEnded(event['request'], event['session'])
            response = buildResponse(sessionAttributes, speechlet)

        # Return a response for speech output
        return(response)

# Called when the session starts
def onSessionStarted(requestId, session):
    print("onSessionStarted requestId=" + requestId + ", sessionId=" + session['sessionId'])

# Called when the user launches the skill without specifying what they want.
def onLaunch(launchRequest, session):
    # Dispatch to your skill's launch.
    getWelcomeResponse()

# Called when the user specifies an intent for this skill.
def onIntent(intentRequest, session, nest):
    intent = intentRequest['intent']
    intentName = intentRequest['intent']['name']

    # Dispatch to your skill's intent handlers
    if intentName == "StateIntent":
        return stateIntent(intent, nest)
    elif intentName == "ChangeIntent":
        return changeIntent(intent, nest)
    elif intentName == "PowerIntent":
        return powerIntent(intent, nest)
    elif intentName == "HelpIntent":
        return getWelcomeResponse()
    else:
        print "Invalid Intent (" + intentName + ")"
        raise

# Called when the user ends the session.
# Is not called when the skill returns shouldEndSession=true.
def onSessionEnded(sessionEndedRequest, session):
    # Add cleanup logic here
    print "Session ended"

def stateIntent(intent, nest):
    repromptText = "Ask the Nest what the temperature is"
    shouldEndSession = True

    temp = nest.get_temp()

    speechOutput = "Your Nest is set to " + str(temp) + " degrees."
    cardTitle = speechOutput

    repromptText = "I didn't understand that. You can say ask the nest what the temperature is, or, ask the nest to set it to 72."
    shouldEndSession = True

    return(buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession))

def changeIntent(intent, nest):
    repromptText = "You can say change my Nest to 72 degrees."
    shouldEndSession = True
    temperature = intent['slots']['temperature']['value']

    nest.set_temp(int(temperature))

    speechOutput = "Ok, I'm setting your Nest to " + str(temperature) + " degrees."
    cardTitle = speechOutput

    repromptText = "I didn't understand that. You can say ask the Nest what the temperature is, or, ask the nest to set it to 72."
    shouldEndSession = True

    return(buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession))

def powerIntent(intent, nest):
    repromptText = "You can say, ask my nest to turn up the heat"
    shouldEndSession = True
    power = intent['slots']['powermode']['value']

    status = nest.get_status()
    if status['target_temperature_type'] == "heat":
        action_type = "heater"
    elif status['target_temperature_type'] == "cool":
        action_type = "air conditioner"
    else:
        action_type = "nest"

    if power == "on":
        nest.turn_on()
        speechOutput = "Ok, I'm turning your " + action_type + " " + power
    elif power == "off":
        nest.turn_off()
        speechOutput = "Ok, I'm turning your " + action_type + " " + power
    else:
        speechOutput = "I wasn't able to do that."

    cardTitle = speechOutput
    repromptText = "You can say ask the Nest to turn the heat on"
    shouldEndSession = True

    return(buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession))


def getWelcomeResponse():
    sessionAttributes = {}
    cardTitle = "Welcome"
    speechOutput = """You can control your Nest by saying, set my Nest to 72 degrees."""

    # If the user either does not reply to the welcome message or says something that is not
    # understood, they will be prompted again with this text.
    repromptText = 'You can control your Nest by saying, set my Nest to 72 degrees.'
    shouldEndSession = True

    return (buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession))

# --------------- Helpers that build all of the responses -----------------------
def buildSpeechletResponse(title, output, repromptText, shouldEndSession):
    return ({
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": "SessionSpeechlet - " + title,
            "content": "SessionSpeechlet - " + output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": repromptText
            }
        },
        "shouldEndSession": shouldEndSession
    })

def buildResponse(sessionAttributes, speechletResponse):
    return ({
        "version": "1.0",
        "sessionAttributes": sessionAttributes,
        "response": speechletResponse
    })

class Nest:
    def __init__(self, username, password, serial = None, index = 1, units="F"):
        self.username   = username
        self.password   = password
        self.serial     = serial
        self.index      = index
        self.units      = units

    def login(self):
        data = urllib.urlencode({"username": self.username, "password": self.password})

        req = urllib2.Request("https://home.nest.com/user/login", data, {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4"})
        res = json.loads(urllib2.urlopen(req).read())

        self.transport_url = res["urls"]["transport_url"]
        self.access_token = res["access_token"]
        self.userid = res["userid"]

        req = urllib2.Request(self.transport_url + "/v2/mobile/user." + self.userid,
                              headers={"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                                       "Authorization":"Basic " + self.access_token,
                                       "X-nl-user-id": self.userid,
                                       "X-nl-protocol-version": "1"})

        res = json.loads(urllib2.urlopen(req).read())
        self.structure_id = res["structure"].keys()[0]

        if (self.serial is None):
            self.device_id = res["structure"][self.structure_id]["devices"][self.index]
            self.serial = self.device_id.split(".")[1]

        self.status = res

    def temp_in(self, temp):
        if (self.units == "F"):
            return (temp - 32.0) / 1.8
        else:
            return temp

    def temp_out(self, temp):
        if (self.units == "F"):
            return (temp * 1.8) + 32.0
        else:
            return temp

    def get_temp(self):
        temp = self.status["shared"][self.serial]["current_temperature"]
        temp = self.temp_out(temp)
        return "%0.1f" % temp

    def set_temp(self, temp):
        temp = self.temp_in(temp)

        data = '{"target_change_pending":true,"target_temperature":' + '%0.1f' % temp + '}'
        req = urllib2.Request(self.transport_url + "/v2/put/shared." + self.serial,
                              data,
                              {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                               "Authorization":"Basic " + self.access_token,
                               "X-nl-protocol-version": "1"})

        res = urllib2.urlopen(req).read()
        return res

    def get_status(self):
        shared = self.status["shared"][self.serial]
        device = self.status["device"][self.serial]

        allvars = shared
        allvars.update(device)

        return allvars

    def turn_off(self):
        allvars = self.get_status()
        current_temperature_f = self.temp_out(allvars["current_temperature"])
        if allvars["target_temperature_type"] == "heat":
            self.set_temp(current_temperature_f - 1)
        elif allvars["target_temperature_type"] == "cool":
            self.set_temp(current_temperature_f + 1)

    def turn_on(self):
        allvars = self.get_status()
        current_temperature_f = self.temp_out(allvars["current_temperature"])
        if allvars["target_temperature_type"] == "heat":
            self.set_temp(current_temperature_f + 1)
        elif allvars["target_temperature_type"] == "cool":
            self.set_temp(current_temperature_f - 1)
