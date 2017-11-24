# Get NewYorkTimes news articles
# Build by Tea

from bs4 import BeautifulSoup
import lxml
import requests as r
import datetime as d
import re
import pymongo


def connectToMongo(db, collection):
    uri = 'mongodb://127.0.0.1/'
    mydb = pymongo.MongoClient(uri)[db][collection]
    return mydb


# Get article list from daily news, give a date in yyyy/mm/dd format
def getArticlesByDate(date):
    daily_url = 'http://www.nytimes.com/indexes/%s/todayspaper/index.html' % (
        date)
    res = r.get(daily_url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    articles = soup.select('.aColumn h6 a') + soup.select('.aColumn h3 a') + \
        soup.select('#SpanABMiddleRegion h6 a')
    return articles


def updateCheckList(ndays):
    for daygap in range(0, ndays):
        date = (d.date.today() - d.timedelta(daygap)).strftime('%Y/%m/%d')
        articles = getArticlesByDate(date)
        CheckList = connectToMongo('checklist', 'articles')
        for article in articles:
            articleInfos = {
                'title': article.text.strip(),
                'date': date,
                'source': 'NewYorkTimes',
                'url': article['href'],
                'isRead': False
            }
            result = CheckList.find_one({'title':articleInfos['title']})
            if len(result) == 0:
                CheckList.insert_one(articleInfos)
                print('inserted: ', articleInfos['date'], articleInfos['title'])
    return print('Update Finished.')


# Get a signle article content
def getArticleInfosAndInsert(uid, aurl):
    res = r.get(aurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')

    try:
        adate = soup.select('.dateline')[0]['content'].split('T')[0]
    except:
        adate = d.datetime.today().strftime('%Y/%m/%d')

    atitle = soup.title.text.split(' - ')[0].strip()

    body = soup.select('.story-body-text')
    acontent = {}
    for numPara in range(len(body)):
        para = re.sub("[“”’]", '\'', body[numPara].text.strip())
        acontent.update({str(numPara + 1): para})

    articleInfos = {
        '_id': uid,
        'title': atitle,
        'date': adate,
        'source': 'NewYorkTimes',
        'url': aurl,
        'content': acontent
    }

    return articleInfos


def goCrawler():
    CheckList = connectToMongo('checklist', 'articles')
    News = connectToMongo('news', 'articles')

    unReadList = CheckList.find({'isRead': False}, {'_id': 1, 'url': 1})

    for element in unReadList:
        articleInfos = getArticleInfosAndInsert(element['_id'], element['url'])
        News.insert_one(articleInfos)
        CheckList.update_one({'_id': articleInfos['_id']}, {'$set': {'isRead': True}})