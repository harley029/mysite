from .models import News

import requests
from bs4 import BeautifulSoup
import lxml


def save_function(article_list):
    News.objects.all().delete()
    for article in article_list:
            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    description = article['description'],
                )
            except Exception as e:
                print(e)
                break
    return print('finished')

def news_rss():
    
    article_list = []

    try:
        print('Starting the scraping tool')
        r = requests.get('https://www.rbc.ua/static/rss/ukrnet.strong.ukr.rss.xml')
        soup = BeautifulSoup(r.content, features='xml')

        articles = soup.findAll('item')

        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            description=a.find("description").text

            article = {
                'title': title,
                'link': link,
                'description':description
            }

            article_list.append(article)
        print('Finished scraping the articles')

        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)
