"""
Original author: xnaas (2022)
License: The Unlicense (public domain)
"""
import re
import requests
from html import unescape
from sopel import plugin
from sopel.modules import url as sopel_url


def hackernews_loader(settings):
    return [re.compile(r"https?://news\.ycombinator\.com/item\?id=(?P<hnid>\d+)")]


@plugin.url_lazy(hackernews_loader)
@plugin.output_prefix('[HackerNews] ')
def get_hn(bot, trigger):
    hnid = trigger.group('hnid')
    url = f"https://hacker-news.firebaseio.com/v0/item/{hnid}.json"
    try:
        r = requests.get(url)
    except Exception:
        try:
            title = sopel_url.find_title(trigger.group(0))
            return bot.say(f"[TITLE ONLY FALLBACK] {title}")
        except Exception:
            return

    if not r.json():
        return

    if r.json()['type'] == 'story':
        title = r.json()['title']
        if 'url' in r.json():
            post_url = r.json()['url']
        elif 'text' in r.json():
            post_url = None
            text = unescape(r.json()['text'])
        return bot.say(f"{title} | {post_url or text}", truncation=' […]')

    if r.json()['type'] == 'comment':
        text = unescape(r.json()['text'])
        return bot.say(text, truncation=' […]')
