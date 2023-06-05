# RSS to Webhook Python

Parses feeds using [feedparser](https://pypi.org/project/feedparser/) and POSTS new entries to a webhook.  
Currently this script sends only `title`, `content`, and `link`, of any new entries, but others could be easily added.

It uses environment variables to configure behaviour. Below are the available env variables:  

`FEEDS` a comma seperated list of compatible feeds:  
```
FEEDS="http://github.com/RocketChat/Rocket.Chat/releases.atom,https://about.gitlab.com/security-
releases.xml"
```

`WEBHOOK` a comma seperated list of compatible feeds:  
```
WEBHOOK="https://chat.internet.com/hooks/etc"
```

`MINUTES` is an the amount of time between updates. Posts newer than this many minutes ago are sent to the webhook.
```
MINUTES="5"
```
