from pymongo import MongoClient
from Chatbot.naver_open_api import *

client = MongoClient('localhost',27017)
#database
db = client.Chatbot


def insert_data(local_data):
    items = search_resturant(local_data)

    for item in items:
        item.setdefault('local_data', local_data)
        db.resturant.insert_one(item)

    # dict
    return items


def find_data_by_location(keyword):
    found_data = list(db.resturant.find({'local_data':keyword}))

    if(len(found_data) == 0):
         print('데이터 없음!')
         res = insert_data(keyword)
         return res

    else:
        print('데이터 존재!')
        return found_data


if __name__ == '__main__':
    print(find_data_by_location('홍대 저녁'))