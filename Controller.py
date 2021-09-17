# -*- conding: utf-8 -*-
import math

from flask import Flask, request, jsonify
from mongo_controller import *
import ssl

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

    elif query_result.get('intent').get('displayName') == 'ButtonClickedEvent':

        queryResult = req.get('queryResult')
        fulfillmentMessages = queryResult.get('fulfillmentMessages')
        platform = fulfillmentMessages[1].get('platform')

        queryText = query_result.get('queryText')
        queryText, _ = queryText.split(" 맛집을 검색합니다!")
        keyword = queryText

        resturant_list = find_data_by_button(keyword)


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
                    "postback": randCards[0]['Title'] + "에 전화를 걸고 싶습니다!"
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
        print(title)
        Tel = find_phoneNum_by_title(title)
        print(Tel)
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
                break
        randCards = find_by_place_and_menu(loc, menu)
        #Error Msg
        if len(randCards) == 0:
            Card1 = {
                "title": '해당하는 식당이 없어요ㅜ^ㅜ',
                # 3줄이 최대
                "subtitle": '찾으시려는 식당이 존재하지 않아요',
                "imageUri": 'https://cdn.dribbble.com/users/1013019/screenshots/3281397/icon_nodata_dribbble.jpg?compress=1&resize=400x300',
                "buttons": [
                    {
                        "text": "릉이 추천 맛집 보기",
                        "postback": '릉이 추천 맛집을 보고 싶어요!'
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
                    "postback": randCards[0]['Title'] + "에 전화를 걸고 싶습니다!"
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

    elif query_result.get('intent').get('displayName') == 'LocoMenux3 - CallResturant':
        title, _ = query_result['queryText'].split('에 전화를 걸고 싶습니다!')
        print(title)
        Tel = find_phoneNum_by_title(title)
        print(Tel)
        return jsonify({
            "fulfillmentMessages": [
                {
                    'text': {'text': ['식당 전화번호: ' + Tel+'\n전화 번호 누를 시 연결됩니다.']},
                    "platform": 'LINE'
                },

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
        # Error Msg
        if len(randCards) == 0:
            Card1 = {
                "title": '해당하는 식당이 없어요ㅜ^ㅜ',
                # 3줄이 최대
                "subtitle": '찾으시려는 식당이 존재하지 않아요',
                "imageUri": 'https://cdn.dribbble.com/users/1013019/screenshots/3281397/icon_nodata_dribbble.jpg?compress=1&resize=400x300',
                "buttons": [
                    {
                        "text": "릉이 추천 맛집 보기",
                        "postback": '릉이 추천 맛집을 보고 싶어요!'
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
                },
                {
                    "text":"전화 걸기",
                    "postback": randCards[0]['Title'] + "에 전화를 걸고 싶습니다!"
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

    elif query_result.get('intent').get('displayName') == 'LocxMenuo3 - CallResturant':
        title, _ = query_result['queryText'].split('에 전화를 걸고 싶습니다!')
        print(title)
        Tel = find_phoneNum_by_title(title)
        print(Tel)
        return jsonify({
            "fulfillmentMessages": [
                {
                    'text': {'text': ['식당 전화번호: ' + Tel+'\n전화 번호 누를 시 연결됩니다.']},
                    "platform": 'LINE'
                },

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
        #Error Msg
        if len(randCards) == 0:
            Card1 = {
                "title": '해당하는 식당이 없어요ㅜ^ㅜ',
                # 3줄이 최대
                "subtitle": '찾으시려는 식당이 존재하지 않아요',
                "imageUri": 'https://cdn.dribbble.com/users/1013019/screenshots/3281397/icon_nodata_dribbble.jpg?compress=1&resize=400x300',
                "buttons": [
                    {
                        "text": "릉이 추천 맛집 보기",
                        "postback": '릉이 추천 맛집을 보고 싶어요!'
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
                },
                {
                    "text":"전화 걸기",
                    "postback": randCards[0]['Title'] + "에 전화를 걸고 싶습니다!"
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

    elif query_result.get('intent').get('displayName') == 'LocoMenuo - CallResturant':
        title, _ = query_result['queryText'].split('에 전화를 걸고 싶습니다!')
        print(title)
        Tel = find_phoneNum_by_title(title)
        print(Tel)
        return jsonify({
            "fulfillmentMessages": [
                {
                    'text': {'text': ['식당 전화번호: ' + Tel+'\n전화 번호 누를 시 연결됩니다.']},
                    "platform": 'LINE'
                },

            ]
        })

    elif query_result.get('intent').get('displayName') == 'AnotherData':
        keyword = random.sample(GangneungIndex, 1)
        print(keyword)
        resturant_list = find_data_by_button(keyword[0])

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
                    "postback": randCards[0]['Title'] + "에 전화를 걸고 싶습니다!"
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



if __name__ == '__main__':
    print("Hello ChatBot")
    app.run(host='0.0.0.0', port="443", ssl_context="adhoc")
