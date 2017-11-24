import pymongo
import re

def connectToMongo(db, collection):
    uri = 'mongodb://127.0.0.1/'
    mydb = pymongo.MongoClient(uri)[db][collection]
    return mydb

def deleteEmptyContent(article):
    if len(article['content']) == 0:
        News.delete_one({'_id': article['_id']})
    return True

def modifyContent(article):
    for para_id in article['content'].keys():
        para = article['content'][para_id]
        new_para = re.sub("[“”’]",'\'', para)
        News.find_one_and_update({'_id':article['_id']},{'$set':{'content.%s'%(para_id):new_para}})
    print('%s is done'%(article['_id']))

def modifyTitle(article):
    title = article['title']
    new_title = re.sub("[“”’]",'\'', title)
    News.find_one_and_update({'_id':article['_id']},{'$set':{'title':new_title}})

News = connectToMongo('news','article')
articles = News.find()
count=1
for article in articles:
    if deleteEmptyContent(article):
        pass
    else:
        modifyContent(article)
        modifyTitle(article)
        print('done:' , count)
        count+=1