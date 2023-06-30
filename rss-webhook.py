#!/usr/bin/python3

import feedparser
import datetime
import json
import requests
import argparse
import sqlite3
import hashlib

def DbPop():

    con = sqlite3.connect("webhook.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS rss(feed, id, hash)")

    return con


def PostHook(jsonEntry, webhook):
    response = requests.post(
        webhook, data=json.dumps(jsonEntry),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        print('Request to webhook returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )


def GetFeeds(feeds, webhook, entries, database):
    cur = database.cursor()
    now = datetime.datetime.now()
    for feed in feeds:
        parsedFeeds = feedparser.parse(feed)
        entInt = entries
        for entry in parsedFeeds.entries:
            storedEntry = "%s + %s" % (entry.id, entry.title)
            m = hashlib.sha256(storedEntry.encode())
            res = database.execute("SELECT hash FROM rss where hash='%s'" % (m.hexdigest()))
            if not res.fetchone():
                newEntry = {
                    "title": entry.title,
                    "content": entry.content,
                    "link": entry.link
                }
                if entInt > 0:
                    print("%s - Posting new entry - '%s'" % (now, entry.link))
                    PostHook(newEntry, webhook)
                    entInt = entInt-1
                cur.execute("""INSERT INTO rss VALUES 
                        ('%s', '%s', '%s')""" % (feed, entry.id, m.hexdigest()))
                database.commit()
            else:
                print("%s - No new entries for feed: %s" % (now, feed))
                break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--feed", required=True,
        action="append", help="feedparser compatible feed")
    parser.add_argument("-w", "--webhook", required=True,
        help="webhook to post to")
    parser.add_argument("-e", "--entries", type=int,
        default=1, help="number of new recent entries to post (default: 1)")

    args = parser.parse_args()

    GetFeeds(args.feed, args.webhook, args.entries, DbPop())

if __name__ == "__main__":
    main()
