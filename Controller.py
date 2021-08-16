# -*- conding: utf-8 -*-
from flask import Flask, request, jsonify

import random

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook(originalDetectIntentRequest=None):
    req = request.get_json(silent=True, force=True)

    print(req)
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


    # If StartIntent Matched
    elif query_result.get('intent').get('displayName') == 'StartIntent':

        # 5개가 중복없이 뽑힌다.
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

                #카드 형식의 첫번쨰 버튼
                {
                    #버튼에 보일 텍스트
                    "text": randIndx[0],
                    #버튼이 눌렀을 때 넘오는 값
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
        #Json 형식으로 반환
        return jsonify({
                "fulfillmentMessages": [
                    #카드 형식으로 보내기
                    {
                        "card":newCard,
                        "platform": platform
                    },

                    #텍스트 형시으로 보내기
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



if __name__ == '__main__':
    print("Hello ChatBot")
    app.run(host='0.0.0.0', port=5000)

