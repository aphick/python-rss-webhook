# RSS to Webhook Python

Parses feeds using [feedparser](https://pypi.org/project/feedparser/) and POSTS new entries to a webhook.  
Currently this script sends only `title`, `content`, and `link`, of any new entries, but others could be easily added.

It uses flags to configure behaviour. Below are the available flags:  

`-f FEED, --feed FEED` A feedparser compatible feed.


`-w WEBHOOK, --webhook WEBHOOK` is the webhook url to post new entries to.


`-m MINUTES, --minutes MINUTES` is an the amount of time between updates. Posts newer than this many minutes ago are sent to the webhook.

```
./rss-webhook.py -f 'http://github.com/RocketChat/Rocket.Chat/releases.atom' -f 'https://about.gitlab.com/security-releases.xml' -w 'https://chat.internet.com/hooks/etc' -m 1440
```
