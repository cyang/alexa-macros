"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "getMacroNutritionIntent":
        return get_macros(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif (intent_name == "AMAZON.StopIntent" or
            intent_name == "AMAZON.CancelIntent"):
        return get_halt_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Macro Nutrition skill. " \
                    "Please tell me your body weight and total calories by saying, " \
                    "get macros for 140 calories and 2500 calories."

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your body weight and total calories by  saying, " \
                    "get macros for 140 calories and 2500 calories."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_halt_response():
    """Stops skill"""
    return build_response({}, build_speechlet_response(
        "Macro Nutrition skill has been canceled", "", "", True))

def get_macros(intent, session):
    '''
    Conversion
    9 calories/1g fat
    4 calories/1g protein
    4 calories/1g carb
    Macros
    fat_range = .20 to .30
    - Ideal is .25 or 25%
    grams_protein = 1g protein per lb body weight
    grams_fat = total_calories * fat_range / (9 calories/1g fat)
    grams_carbs = (total_calories - grams_protein * (4 calories/1g protein) - grams_fat * (9 calories/1g fat)) / (4 calories/1g carb)
    Example
    total_calories = 2420 calories
    body_weight = 135 lb
    grams_protein = 135g
    grams_fat = 2420 * .25 / 9 = 67.2222g
    grams_carbs = (2420 - (135 * 4) - (67.2222 * 9))/4 = 318.7501g
    '''

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'totalCalories' in intent['slots'] and 'bodyWeight' in intent['slots']:
        slots = intent['slots']
        total_calories = float(slots['totalCalories']['value'])
        body_weight = float(slots['bodyWeight']['value'])
        fat_range = 0.25
        grams_protein = body_weight
        grams_fat = total_calories * fat_range / 9
        grams_carbs = (total_calories - (grams_protein * 4) - (grams_fat *9))/4

        speech_output  = '%d grams of protein, %d grams of carbs, and %d grams of fat' % (grams_protein, grams_carbs, grams_fat)
        reprompt_text = ""
    else:
        speech_output = "I'm not sure what your body weight and total calories  are. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your body weight and total calories  are. " \
                        "You can tell me your body weight and total calories by saying, " \
                        "get macros for 140 calories and 2500 calories."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
