# -*- conding: utf-8 -*-
import math

from flask import Flask, request, jsonify
from mongo_controller import *

import random

app = Flask(__name__)

def make_Rating(r):
    r = float(r)
    res = ''
    for i in range(math.floor(r)):
        res += '★'
    if r - math.floor(r) >= 0.5:
        res += '☆'
    res += " ("
    res += str(r)
    res += ")"
    return res

@app.route('/webhook', methods=['POST'])
def webhook(originalDetectIntentRequest=None):
    req = request.get_json(silent=True, force=True)

    print(req)
    query_result = req.get('queryResult')

    GangneungIndex = ['강릉 중앙 시장', '경포대', '주문진', '정동진', '오대산', '안목 해변',
                      '교동 짬뽕', '커피', '장칼국수', '곰치국', '빵', '수제 버거', '초당 순두부',
                      '회', '옹심이', '막국수', '섭국']
    Indicies = list(range(len(GangneungIndex)))

    # 시작 이벤트
    if query_result.get('intent').get('displayName') == 'StartIntent':

        # 5개가 중복없이 뽑힌다.
        randIndx = random.sample(Indicies, 4)
        print(randIndx)

        queryResult = req.get('queryResult')
        print(queryResult)
        fulfillmentMessages = queryResult.get('fulfillmentMessages')
        platform = fulfillmentMessages[1].get('platform')
        card = fulfillmentMessages[1].get('card')
        title = card.get("title")
        subtitle = card.get("subtitle")
        imageUri = card.get("imageUri")
        newCard = {
            "title":title,
            #3줄이 최대
            "subtitle": subtitle,
            "imageUri": imageUri,
            "buttons":[

                #카드 형식의 첫번쨰 버튼
                {
                    #버튼에 보일 텍스트
                    "text": GangneungIndex[randIndx[0]],
                    #버튼이 눌렀을 때 넘오는 값
                    "postback": GangneungIndex[randIndx[0]] + " 맛집을 검색합니다!"
                },
                {
                    "text": GangneungIndex[randIndx[1]],
                    "postback": GangneungIndex[randIndx[1]] + " 맛집을 검색합니다!"
                },
                {
                    "text": GangneungIndex[randIndx[2]],
                    "postback": GangneungIndex[randIndx[2]] + " 맛집을 검색합니다!"
                },
                {
                    "text": GangneungIndex[randIndx[3]],
                    "postback": GangneungIndex[randIndx[3]] + " 맛집을 검색합니다!"
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

                ]
        })

    # 버튼 클릭 이벤트
    elif query_result.get('intent').get('displayName') == 'ButtonClickedEvent':

        queryResult = req.get('queryResult')
        fulfillmentMessages = queryResult.get('fulfillmentMessages')
        platform = fulfillmentMessages[1].get('platform')

        queryText = query_result.get('queryText')
        queryText, _ = queryText.split(" 맛집을 검색합니다!")
        keyword = queryText

        resturant_list = find_data_by_button(keyword)

        if len(resturant_list) == 0:
            return jsonify({
                "fulfillmentMessages": [
                    # 카드 형식으로 보내기
                    {
                        "text":{
                            "text":"No Data"
                        },
                        "platform": 'LINE'
                    }
                ]

            })

        randCards = random.sample(resturant_list, 2)
        print(randCards[0]['Title'], randCards[1]['Title'])
        Card1 = {
            "title": randCards[0]['Title'],
            # 3줄이 최대
            "subtitle": make_Rating(randCards[0]['Rating']) + "\n" + randCards[0]['Price'] + "\n" + randCards[0]['Open_Close'],
            "imageUri": randCards[0]['ImgLink'],
             "buttons": [
                 {
                     "text": "네이버 지도로 보기",
                     "postback": randCards[0]['MapSearchUrl']
                 },
                {
                    "text":"전화 걸기",
                    "postback": randCards[0]['Title'] + "식당에 전화를 걸고 싶습니다!"
                }
             ]

        }
        Card2 = {
            "title": randCards[1]['Title'],
            # 3줄이 최대
            "subtitle": make_Rating(randCards[1]['Rating']) + "\n" + randCards[1]['Price'] + "\n" + randCards[1][
                'Open_Close'],
            "imageUri": randCards[1]['ImgLink'],

            "buttons": [

                {
                    "text": "네이버 지도로 보기",
                    "postback": randCards[1]['MapSearchUrl']
                },
                {
                    "text":"전화 걸기",
                    "postback": randCards[1]['Title'] + "에 전화를 걸고 싶습니다!"
                }
            ]

        }
        # Json 형식으로 반환
        return jsonify({
            "fulfillmentMessages": [
                # 카드 형식으로 보내기
                {
                    "card": Card1,
                    "platform": 'LINE'
                },

                # 카드 형식으로 보내기
                {
                    "card": Card2,
                    "platform": 'LINE'
                }
            ]
        })

    elif query_result.get('intent').get('displayName') == 'ButtonClickedEvent - CallResturant':
        title, _ = query_result['queryText'].split('에 전화를 걸고 싶습니다!')
        Tel = find_phoneNum_by_title(title)
        return jsonify({
            "fulfillmentMessages": [
                {
                    'text': {'text': ['식당 전화번호: ' + Tel+'\n전화 번호 누를 시 연결됩니다.']},
                    "platform": 'LINE'
                },

            ]
        })

    elif query_result.get('intent').get('displayName') == 'LocoMenux2':
        print(query_result)
        #List or Str
        menu = query_result.get('parameters')['Food']
        if type(menu) != str:
            menu = menu[0]
        outputContexts = query_result.get('outputContexts')

        loc = ''
        for context in outputContexts:
            if context['name'][-10:] == "locomenux1":
                loc = context['parameters']['Region']
                print(loc)
                break
        randCards = find_by_place_and_menu(loc, menu)
        Card1 = {
            "title": randCards[0]['Title'],
            # 3줄이 최대
            "subtitle": make_Rating(randCards[0]['Rating']) + "\n" + randCards[0]['Price'] + "\n" + randCards[0]['Open_Close'],
            "imageUri": randCards[0]['ImgLink'],
            "buttons": [
                {
                    "text": "네이버 지도로 보기",
                    "postback": randCards[0]['MapSearchUrl']
                }
            ]

        }

        return jsonify({
            "fulfillmentMessages": [
                # 카드 형식으로 보내기
                {
                    "card": Card1,
                    "platform": 'LINE'
                }
            ]
        })

    elif query_result.get('intent').get('displayName') == 'LocxMenuo2':
        print(query_result)
        #List or Str
        loc = query_result.get('parameters')['Region']
        if type(loc) != str:
            loc = loc[0]
        print("location", loc)
        outputContexts = query_result.get('outputContexts')
        menu = ''
        print(outputContexts)

        for context in outputContexts:
            if context['name'][-10:] == "locxmenuo1":
                menu = context['parameters']['Food']
                print(menu)
                break
        randCards = find_by_place_and_menu(loc, menu)
        Card1 = {
            "title": randCards[0]['Title'],
            # 3줄이 최대
            "subtitle": make_Rating(randCards[0]['Rating']) + "\n" + randCards[0]['Price'] + "\n" + randCards[0][
                'Open_Close'],
            "imageUri": randCards[0]['ImgLink'],
            "buttons": [
                {
                    "text": "네이버 지도로 보기",
                    "postback": randCards[0]['MapSearchUrl']
                }
            ]

        }

        return jsonify({
            "fulfillmentMessages": [
                # 카드 형식으로 보내기
                {
                    "card": Card1,
                    "platform": 'LINE'
                }
            ]
        })

    elif query_result.get('intent').get('displayName') == 'LocoMenuo':
        loc = query_result.get('parameters')['Region']
        if type(loc) != str:
            loc = loc[0]
        menu = query_result.get('parameters')['Food']
        if type(menu) != str:
            menu = loc[0]
        randCards = find_by_place_and_menu(loc, menu)
        Card1 = {
            "title": randCards[0]['Title'],
            # 3줄이 최대
            "subtitle": make_Rating(randCards[0]['Rating']) + "\n" + randCards[0]['Price'] + "\n" + randCards[0][
                'Open_Close'],
            "imageUri": randCards[0]['ImgLink'],
            "buttons": [
                {
                    "text": "네이버 지도로 보기",
                    "postback": randCards[0]['MapSearchUrl']
                }
            ]

        }

        return jsonify({
            "fulfillmentMessages": [
                # 카드 형식으로 보내기
                {
                    "card": Card1,
                    "platform": 'LINE'
                }
            ]
        })

# a = {'queryText': '장칼국수',
#     'action': 'LocoMenux1.LocoMenux1-custom',
#     'parameters': {},
#      'allRequiredParamsPresent': True,
#      'fulfillmentMessages': [
#          {'card': {'title': 'LocoMenux2',
#                    'subtitle': 'LocoMemux2인텐트',
#                    'imageUri': 'https://img.siksinhot.com/place/1548828274568053.jpg?w=307&h=300&c=Y',
#                    'buttons': [
#                        {'text': 'LocoMenux2',
#                         'postback': 'https://www.google.com/search?q=%EA%B2%BD%ED%8F%AC%EC%A0%95%EC%9C%A1%EC%A0%90%EC%8B%9D%EB%8B%B9%EC%95%A4%EC%A1%B0%EA%B0%9C%EA%B5%AC%EC%9D%B4&sxsrf=ALeKk0140eU3ywowHwlce9I0VKNIsmPzLA:1629614058344&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjq1cW4gcTyAhXbyYsBHXeYDZ4Q_AUoAXoECAEQAw&biw=2048&bih=962#imgrc=y-8nKfJ33SLCkM'
#                         }
#                         ]
#                      },'platform': 'LINE'},
#                     {'text': {'text': ['']}
#                     }
#                     ],
#                     'outputContexts': [
#                         {'name': 'projects/gangneung-sscq/agent/sessions/b20f697d-4fb8-3270-9f21-6b0d4c4ec97f/contexts/locomenux1',
#                          'lifespanCount': 5,
#                          'parameters': {'Button_name': 'Button',
#                          'Button_name.original': 'button1',
#                          'Region': '경포대', 'Region.original': '경포대'}
#                          },
#                         {'name': 'projects/gangneung-sscq/agent/sessions/b20f697d-4fb8-3270-9f21-6b0d4c4ec97f/contexts/startintent',
#                          'lifespanCount': 5,
#                          'parameters': {'Button_name': 'Button', 'Button_name.original': 'button1', 'Region': '경포대', 'Region.original': '경포대'}},
#                         {'name': 'projects/gangneung-sscq/agent/sessions/b20f697d-4fb8-3270-9f21-6b0d4c4ec97f/contexts/research',
#                          'lifespanCount': 5,
#                          'parameters': {'Button_name': 'Button', 'Button_name.original': 'button1', 'Region': '경포대', 'Region.original': '경포대'}},
#                         {'name': 'projects/gangneung-sscq/agent/sessions/b20f697d-4fb8-3270-9f21-6b0d4c4ec97f/contexts/locomenux2-followup', 'lifespanCount': 2},
#                         {'name': 'projects/gangneung-sscq/agent/sessions/b20f697d-4fb8-3270-9f21-6b0d4c4ec97f/contexts/locomenux1-followup', 'lifespanCount': 1,
#                          'parameters': {'Region': '경포대', 'Region.original': '경포대'}},
#                         {'name': 'projects/gangneung-sscq/agent/sessions/b20f697d-4fb8-3270-9f21-6b0d4c4ec97f/contexts/locomenuo',
#                          'lifespanCount': 2, 'parameters': {'Button_name': 'Button', 'Button_name.original': 'button1', 'Region': '경포대', 'Region.original': '경포대'}},
#                         {'name': 'projects/gangneung-sscq/agent/sessions/b20f697d-4fb8-3270-9f21-6b0d4c4ec97f/contexts/locxmenuo1', 'lifespanCount': 2,
#                          'parameters': {'Button_name': 'Button', 'Button_name.original': 'button1', 'Region': '경포대', 'Region.original': '경포대'}},
#                         {'name': 'projects/gangneung-sscq/agent/sessions/b20f697d-4fb8-3270-9f21-6b0d4c4ec97f/contexts/locomenux2', 'lifespanCount': 4, 'parameters': {'Region': '경포대', 'Region.original': '경포대'}},
#                         {'name': 'projects/gangneung-sscq/agent/sessions/b20f697d-4fb8-3270-9f21-6b0d4c4ec97f/contexts/buttonclickedevent',
#                          'lifespanCount': 2, 'parameters': {'Button_name': 'Button', 'Button_name.original': 'button1', 'Region': '경포대', 'Region.original': '경포대'}},
#                         {'name': 'projects/gangneung-sscq/agent/sessions/b20f697d-4fb8-3270-9f21-6b0d4c4ec97f/contexts/locxmenux', 'lifespanCount': 2, 'parameters': {'Button_name': 'Button', 'Button_name.original': 'button1', 'Region': '경포대', 'Region.original': '경포대'}},
#                         {'name': 'projects/gangneung-sscq/agent/sessions/b20f697d-4fb8-3270-9f21-6b0d4c4ec97f/contexts/__system_counters__', 'parameters': {'no-input': 0.0, 'no-match': 0.0}}],
#                         'intent': {'name': 'projects/gangneung-sscq/agent/intents/a0a5551a-f571-4a50-8288-b88fdcc2893d', 'displayName': 'LocoMenux2'}, 'intentDetectionConfidence': 1.0, 'languageCode': 'en'}



if __name__ == '__main__':
    print("Hello ChatBot")
    app.run(host='0.0.0.0', port=5000)

