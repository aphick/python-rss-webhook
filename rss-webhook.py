#!/usr/bin/python3

import feedparser
import os
import datetime
import json
import requests
from time import mktime
import argparse

def PostHook(jsonEntry, webhook):
    response = requests.post(
        webhook, data=json.dumps(jsonEntry),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to webhook returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )


def GetFeeds(feeds, webhook, minutes):
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
                PostHook(newEntry, webhook)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--feed", required=True,
        action="append", help="feedparser compatible feed")
    parser.add_argument("-w", "--webhook", required=True,
        help="webhook to post to")
    parser.add_argument("-m", "--minutes", required=True,
        help="number of minutes since last run")

    args = parser.parse_args()

    GetFeeds(args.feed, args.webhook, args.minutes)

if __name__ == "__main__":
    main()