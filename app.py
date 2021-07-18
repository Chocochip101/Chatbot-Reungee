from flask import Flask, request
from Chatbot.mongo_controller import find_data_by_location

app = Flask(__name__)


@app.route('/')  # this is the home page route
def hello_world():  # this is the home page function that generates the page code
    return "Hello world!"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    fulfillmentText = ''
    query_result = req.get('queryResult')

    print(query_result)
    if query_result.get('intent').get('displayName') == 'LocoMenuoTimeo':
        location = query_result.get('parameters').get('number')
        fulfillmentText = 'This is from my fullfillment of LocoMenuoTimeo'

    elif query_result.get('intent').get('displayName') == 'LocoMenuoTimex':
        fulfillmentText = 'This is from my fullfillment of LocoMenuoTimex'

    elif query_result.get('intent').get('displayName') == 'LocoMenuxTimeo':
        fulfillmentText = 'This is from my fullfillment of LocoMenuxTimeo'

    elif query_result.get('intent').get('displayName') == 'LocoMenuxTimex':
        fulfillmentText = 'This is from my fullfillment of LocoMenuxTimex'

    elif query_result.get('intent').get('displayName') == 'LocxMenuoTimeo':
        fulfillmentText = 'This is from my fullfillment of LocxMenuoTimeo'

    elif query_result.get('intent').get('displayName') == 'LocxMenuoTimex':
        fulfillmentText = 'This is from my fullfillment of LocxMenuoTimex'

    elif query_result.get('intent').get('displayName') == 'LocxMenuoTimex':
        fulfillmentText = 'This is from my fullfillment of LocxMenuxTimex'

    elif query_result.get('intent').get('displayName') == 'LocxMenuxTimeo':
        fulfillmentText = 'This is from my fullfillment of LocxMenuxTimeo'

    elif query_result.get('intent').get('displayName') == 'LocxMenuxTimex':
        fulfillmentText = 'This is from my fullfillment of LocxMenuxTimeo'

    # elif query_result.get('intent').get('displayName') == 'multiply.numbers':
    #     num1 = int(query_result.get('parameters').get('number'))
    #     num2 = int(query_result.get('parameters').get('number1'))
    #     product = str(num1 * num2)
    #     print('here num1 = {0}'.format(num1))
    #     print('here num2 = {0}'.format(num2))
    #     fulfillmentText = 'The product of the two numbers is ' + product
    return {
        "fulfillmentText": fulfillmentText,
        "source": "webhookdata"
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
