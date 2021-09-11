import json
from urllib import parse, request

def search_resturant(location='', menu=''):

    clientId = "VhbUCLMP0G9GktY1da2R"
    clientSecret = "aPV80eOIok"
    # keyword = location + ' ' + time + ' '  + menu

    keyword = location + ' ' + menu
    #변수 keyword URL encoding
    enc_text = parse.quote(keyword)

    #정렬 옵션: random(유사도순), comment(카페/블로그 리뷰 개수 순)
    sort = "comment"

    url = "https://openapi.naver.com/v1/search/local?query=" + enc_text + "&display=10" + "&sort=" + sort

    #HTTP요청 객체 생성
    req = request.Request(url)
    req.add_header("X-Naver-Client-Id", clientId)
    req.add_header("X-Naver-Client-Secret",clientSecret)

    try:
        response = request.urlopen(req)
    except:
        print("{} 검색 불가".format(keyword))
        return None

    res_code = response.getcode()  # response의 코드
    if (res_code == 200):  # 200 OK 이면
        response_body = response.read()

        # print(response_body.decode('utf-8'))
        res = json.loads(response_body.decode('utf-8'))

        # list(dict)
        # 식당명, 링크, 카테고리,요약, 전화번호, 주소, 도로명 주소, x, y
        return res['items']

if __name__ == '__main__':
    print(search_resturant('강릉', '물회'))