from pymongo import MongoClient
import random

client = MongoClient('localhost',27017)

#database
db = client.Gangneung
Collections = db.Resturant



def find_data_by_button(KeyWord):
    result = []

    for data in Collections.find():
        try:
            if KeyWord in data['BtnKeyWord'].split(', '):
                result.append(data)
        except:
            print("DB Error")
    return result


def find_by_place_and_menu(place, menu):
    result = []
    Entire_data = list(Collections.find())

    for data in Entire_data:
        try:
            if place in list(data['Location'].split(', ')) and menu in list(data['Menu'].split(', ')):
                result.append(data)
        except:
            print("DB Error")
    result = random.sample(result, 1)
    print(result)
    return result


if __name__ == '__main__':
    print(find_by_place_and_menu("강릉 중앙 시장", "고구마 어묵고로케"))