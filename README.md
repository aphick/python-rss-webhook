# RSS to Webhook Python

Parses feeds using [feedparser](https://pypi.org/project/feedparser/) and POSTS new entries to a webhook.  
Currently this script sends only `title`, `content`, and `link`, of any new entries, but others could be easily added.

It uses flags to configure behaviour. Below are the available flags:  

`-f FEED, --feed FEED` A feedparser compatible feed.


`-w WEBHOOK, --webhook WEBHOOK` is the webhook url to post new entries to.


`-e ENTRIES, --entries ENTRIES` the number of new entries to post. Defaults to "1" in order to reduce first run activity.

```
./rss-webhook.py -f 'http://github.com/RocketChat/Rocket.Chat/releases.atom' -f 'https://about.gitlab.com/security-releases.xml' -w 'https://chat.internet.com/hooks/etc' -e 2
```
