from django.core.management.base import BaseCommand
import snscrape.modules.twitter as sntwitter
import time
import csv
from celery import shared_task
from serverApi.models import Twitter 

@shared_task
def scrape_tweet():
    #Scrapes the twitter data
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:LiveDrive').get_items()):
        if i>0:
            break
        tweets=[tweet.date, tweet.rawContent]
    
    # print(tweets[0],'\n', tweets[1])

    for item in tweets:
       Twitter.create(**item)
