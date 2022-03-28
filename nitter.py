from sopel import plugin
from sopel_modules import twitter
import re


@plugin.url(r"https?://nitter\.actionsack\.com/(?P<user>\w+)(?:/status/(?P<status>\d+))?")
@plugin.url(r"https?://nitter\.actionsack\.com/i/web/status/(?P<status>\d+).*")
def nitter_to_twitter(bot, trigger, match):
    stuff = match.groupdict()
    tweet = stuff.get("status", None)
    user = stuff.get("user", None)

    try:
        if tweet:
            twitter.output_status(bot, trigger, tweet)
        elif user:
            twitter.output_user(bot, trigger, user)
        else:
            return
    except BaseException:
        return
