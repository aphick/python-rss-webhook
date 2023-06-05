#!/usr/bin/python3

import feedparser
import os
import datetime
import json
import requests
from time import mktime

feeds = os.environ.get('FEEDS').split(',')
minutes = os.environ.get('MINUTES')
webhook = os.environ.get('WEBHOOK')

def PostHook(jsonEntry):
    response = requests.post(
        webhook, data=json.dumps(jsonEntry),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to webhook returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )


def GetFeeds():
    now = datetime.datetime.now()
    lastRun = now - datetime.timedelta(minutes=int(minutes))

    for feed in feeds:
        parsedFeeds = feedparser.parse(feed)
        for entry in parsedFeeds.entries:
            try:
                ptime = entry.published_parsed
            except:
                ptime = entry.updated_parsed
            pubDate = datetime.datetime.fromtimestamp(mktime(ptime))
            if pubDate > lastRun:
                newEntry = {
                    "title": entry.title,
                    "content": entry.content,
                    "link": entry.link
                }
                PostHook(newEntry)

GetFeeds()
