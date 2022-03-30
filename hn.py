from sopel import plugin
from sopel.modules import url as sopel_url
import re
import requests


def hackernews_loader(settings):
    return [re.compile(r"https?://news\.ycombinator\.com/item\?id=(?P<hnid>\d+)")]


@plugin.url_lazy(hackernews_loader)
@plugin.output_prefix("[HackerNews] ")
def get_hn(bot, trigger):
    hnid = trigger.group("hnid")
    url = "https://hacker-news.firebaseio.com/v0/item/{}.json".format(hnid)
    try:
        r = requests.get(url)
    except BaseException:
        try:
            title = sopel_url.find_title(trigger.group(0))
            return bot.say("[TITLE ONLY FALLBACK] {}".format(title))
        except BaseException:
            return

    if not r.json():
        return

    if r.json()["type"] == "story":
        title = r.json()["title"]
        if "url" in r.json():
            post_url = r.json()["url"]
        elif "text" in r.json():
            post_url = None
            text = r.json()["text"]
        return bot.say("{} | {}".format(title, post_url or text), truncation=" […]")

    if r.json()["type"] == "comment":
        text = r.json()["text"]
        return bot.say(text, truncation=" […]")
