# -*- conding: utf-8 -*-
from flask import Flask, request, jsonify, abort

from Chatbot.mongo_controller import find_data, delete_backspace
import random

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook(originalDetectIntentRequest=None):
    req = request.get_json(silent=True, force=True)

    print(req)
    fulfillmentText = ''
    query_result = req.get('queryResult')

    GangneungIndex = ['강릉 중앙 시장', '경포대', '주문진', '정동진', '오대산', '초당 순두부',
                      '교동 짬뽕', '커피', '장칼국수', '곰치국', '송이 요리', '햄버거', '순두부 젤라또',
                      '물회', '옹심이', '막국수', '섭국']

    if query_result.get('intent').get('displayName') == 'ButtonClickedEvent':
        queryText = query_result.get('queryText')
        queryText, _ = queryText.split(' is ')
        queryText = queryText[6:]
        keyword = GangneungIndex[int(queryText) - 1]
        fulfillmentText = '검색하신 버튼은 ' + keyword + '입니다!'

        return {
            "fulfillmentText": str(fulfillmentText),
            "source": "webhookdata"
        }


    #
    elif query_result.get('intent').get('displayName') == 'StartIntent':

        # #5개가 중복없이 뽑힌다.
        randIndx = random.sample(GangneungIndex, 4)
        print(randIndx)

        queryResult = req.get('queryResult')
        fulfillmentMessages = queryResult.get('fulfillmentMessages')
        platform = fulfillmentMessages[0].get('platform')
        card = fulfillmentMessages[0].get('card')
        title = card.get("title")
        subtitle = card.get("subtitle")
        imageUri = card.get("imageUri")
        newCard = {
            "title":title,
            "subtitle": subtitle,
            "imageUri": imageUri,
            "buttons":[
                {
                    "text": randIndx[0],
                    "postback": "button1 is clicked"
                },
                {
                    "text": randIndx[1],
                    "postback": "button2 is clicked"
                },
                {
                    "text": randIndx[2],
                    "postback": "button3 is clicked"
                },
                {
                    "text": randIndx[3],
                    "postback": "button3 is clicked"
                }
            ]
        }

        return jsonify({
                "fulfillmentMessages": [
                    {
                        "card":newCard,
                        "platform": platform
                    },
                    {
                        "text": {
                            "text": [
                                "배안고파"
                            ]
                        },
                        "platform": platform
                    }
                ]
        })


    elif query_result.get('intent').get('displayName') == 'LocoMenuxTimeo':
        location = query_result.get('parameters').get('Region')
        fulfillmentText = 'This is from my fulfillment of LocoMenuxTimeo'

    elif query_result.get('intent').get('displayName') == 'LocoMenuxTimex':
        location = query_result.get('parameters').get('Region')
        fulfillmentText = 'This is from my fulfillment of LocoMenuxTimex'

    elif query_result.get('intent').get('displayName') == 'LocxMenuoTimeo':
        food = query_result.get('parameters').get('Food')
        fulfillmentText = 'This is from my fulfillment of LocxMenuoTimeo'

    elif query_result.get('intent').get('displayName') == 'LocxMenuoTimex':
        food = query_result.get('parameters').get('Food')
        fulfillmentText = 'This is from my fulfillment of LocxMenuoTimex'

    elif query_result.get('intent').get('displayName') == 'LocxMenuoTimex':
        food = query_result.get('parameters').get('Food')
        fulfillmentText = f'This is from my fulfillment of LocxMenuxTimex'

    elif query_result.get('intent').get('displayName') == 'LocxMenuxTimeo':
        fulfillmentText = 'This is from my fulfillment of LocxMenuxTimeo'

    elif query_result.get('intent').get('displayName') == 'LocxMenuxTimex':
        fulfillmentText = 'This is from my fulfillment of LocxMenuxTimeo'

    # elif query_result.get('intent').get('displayName') == 'multiply.numbers':
    #     num1 = int(query_result.get('parameters').get('number'))
    #     num2 = int(query_result.get('parameters').get('number1'))
    #     product = str(num1 * num2)
    #     print('here num1 = {0}'.format(num1))
    #     print('here num2 = {0}'.format(num2))
    #     fulfillmentText = 'The product of the two numbers is ' + product




if __name__ == '__main__':
    print("Hello ChatBot")
    app.run(host='0.0.0.0', port=5000)

