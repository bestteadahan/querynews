import pymongo
import math
import operator


def connectToMongo(db, collection):
    uri = 'mongodb://127.0.0.1/'
    mydb = pymongo.MongoClient(uri)[db][collection]
    return mydb

# Calculate IDF value
def updateIDF(N, DB_wdlist):
    wds = DB_wdlist.find()
    for wd in wds:
        idf = math.log(N/wd['count'])
        DB_wdlist.update_one({'_id': wd['_id']}, {'$set': {'IDF': idf}})
    print('IDF in DB_wdlist updated.')


# Find top 10 keywords by word.TF and IDF in DB_wdlist
def findkeywords(wordset, DB_wdlist):
    tfidf_dict = {}
    for wd in wordset:
        ref = DB_wdlist.find_one({'_id':wd})
        tfidf = wordset[wd]['TF']*ref['IDF']
        tfidf_dict[wd] = tfidf
    kw_TFIDF = sorted(tfidf_dict.items(), key=operator.itemgetter(1), reverse=True)[0:10]
    return dict(kw_TFIDF)


DB_articles = connectToMongo('news','articles')
DB_wdlist = connectToMongo('news','wdlist')

# Update IDF value in DB_wdlist
N = DB_articles.find().count()
updateIDF(N, DB_wdlist)

cursor = DB_articles.find({'keywords': {'$exists': False}}, {'_id':1, 'wordset':1})
while cursor.alive:
    article = cursor.next()
    wordset = article['wordset']
    kw_TFIDF = findkeywords(wordset, DB_wdlist)
    DB_articles.update_one({'_id':article['_id']}, {'$set':{'keywords':kw_TFIDF}}, upsert=True)
    print('ok: ', article['_id'])