from pymongo import MongoClient
from Chatbot.naver_open_api import *

client = MongoClient('localhost',27017)
#database
db = client.Chatbot


def insert_data(local_data='', menu=''):
    items = search_resturant(local_data, menu)

    for item in items:
        item.setdefault('local_data', local_data)
        item.setdefault('menu', menu)
        db.resturant.insert_one(item)

    # dict
    return items


def find_data(local_data='', menu=''):
    found_data = list(db.resturant.find({'local_data':local_data, 'menu':menu}))

    if(len(found_data) == 0):
         print('데이터 없음!')
         res = insert_data(local_data, menu)
         return res

    else:
        print('데이터 존재!')
        return found_data

def delete_backspace(title):
    if '<b>' in title:
        tok1, tok2 = title.split('<b>')
        title = tok1 + tok2
    if '</b>' in title:
        tok1, tok2 = title.split('</b>')
        title = tok1 + tok2
    return title


if __name__ == '__main__':
    print((find_data('강릉','불고기')))