import re
import pymongo
from collections import Counter
from textblob import TextBlob
from textblob import Word


def connectToMongo(db, collection):
    uri = 'mongodb://127.0.0.1/'
    mydb = pymongo.MongoClient(uri)[db][collection]
    return mydb


# Define stopwords
def defineStopWords():
    with open('stop-word-list.txt', 'r', encoding='utf8') as mysw:
        swlist = mysw.read().split(',')
        mysw.close()
    return swlist


# Return all cleaned words in one paragraph
def get_parawds(paraString):
    words = str(TextBlob(paraString).words.lower())
    match = re.findall('[a-z]+', words)
    parawds = []
    for word in match:
        if word not in STOPWDS and len(word) > 2:
            finalWord = Word(word).singularize().lemmatize("v")
            parawds.append(finalWord)
    return parawds


def wc(article):
    content = article['content']

    wd_set = {}
    totalWordsNumber = 0
    for index in content.keys():
        paraString = content[index]
        parawds = get_parawds(paraString)
        totalWordsNumber += len(parawds)
        for wd in parawds:
            if wd not in wd_set.keys():
                wd_set[wd] = {'src':set([index]),'count':1 }
            else:
                wd_set[wd]['src'].add(index)
                wd_set[wd]['count'] += 1

    DB_wdlist = connectToMongo('news','wdlist')

    # Calculating TF value
    for wd in wd_set.keys():
        wd_set[wd]['TF'] = wd_set[wd]['count'] / totalWordsNumber
        wd_set[wd]['src'] = list(wd_set[wd]['src'])
        DB_wdlist.update_one({'_id': wd}, {'$inc': {'count': 1}},upsert=True)

    return wd_set


def goCounter():
    DB_news = connectToMongo('news', 'articles')
    DB_DB_wdlist = connectToMongo('news','wdlist')
    
    cursor = DB_news.find({'isCounted': True})
    while cursor.alive:
        article = cursor.next()
        wd_set = wc(article)
        DB_news.update_one({'_id': article['_id']}, {'$set': {'isCounted': True, 'wordset': wd_set}})
        print('ok  ', article['_id'])



global STOPWDS
STOPWDS = defineStopWords()
goCounter()
print('Word count finished!')