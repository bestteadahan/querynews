import pymongo
import sys
import json
import random

try:
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client['news']
    DB_news = db['articles']
except:
    print('Cannot connect to MongoDB server!')

# 查詢某生詞出處


def findResult(user_input, user_level):
    field = 'wordset.' + user_input
    cursor = DB_news.find({field: {'$exists': True}, 'level': user_level}).limit(10)
    result_list = []
    while (cursor.alive) & (cursor.count()) >=1:
        document = cursor.next()
        src = document['wordset'][user_input]['src']
        para_id = random.choice(src)
        res_dict = {
            'Title': document['title'],
            'Link': document['url'],
            'Paragraph': document['content'][para_id],
            'Level': document['level']
        }
        result_list.append(res_dict)
    return result_list


user_input = sys.argv[1]
user_level = str(sys.argv[2])

result_list = findResult(user_input, user_level)
print(json.dumps(result_list))

client.close()