from sopel import plugin
from sopel_modules import twitter
import re


NITTER_DOMAINS = [
    r"nitter\.net",
    r"nitter\.42l\.fr",
    r"nitter\.pussthecat\.org",
    r"nitter\.nixnet\.services",
    r"nitter\.fdn\.fr",
    r"nitter\.1d4\.us",
    r"nitter\.kavin\.rocks",
    r"nitter\.unixfox\.eu",
    r"nitter\.domain\.glass",
    r"nitter\.eu",
    r"nitter\.namazso\.eu",
    r"nitter\.actionsack\.com",
    r"birdsite\.xanny\.family",
    r"nitter\.hu",
    r"twitr\.gq",
    r"nitter\.moomoo\.me",
    r"nittereu\.moomoo\.me",
    r"bird\.trom\.tf",
    r"nitter\.it",
    r"twitter\.censors\.us",
    r"nitter\.grimneko\.de",
    r"nitter\.alefvanoon\.xyz",
    r"n\.hyperborea\.cloud",
    r"nitter\.ca",
    r"twitter\.076\.ne\.jp",
    r"nitter\.mstdn\.social",
    r"nitter\.fly\.dev",
    r"notabird\.site",
    r"nitter\.weiler\.rocks",
    r"nitter\.silkky\.cloud",
    r"nitter\.sethforprivacy\.com",
    r"nttr\.stream",
    r"nitter\.cutelab\.space",
    r"nitter\.nl",
    r"nitter\.mint\.lgbt",
    r"nitter\.bus-hit\.me",
    r"fuckthesacklers\.network",
    r"nitter\.govt\.land",
    r"nitter\.datatunnel\.xyz",
    r"nitter\.esmailelbob\.xyz",
    r"tw\.artemislena\.eu",
    r"de\.nttr\.stream",
    r"nitter\.winscloud\.net",
    r"nitter\.tiekoetter\.com",
    r"nitter\.spaceint\.fr",
    r"twtr\.bch\.bar"
]


def nitter_loader(settings):
    nitters = []
    for domain in NITTER_DOMAINS:
        nitters.append(re.compile(r"https?://{}/(?P<user>\w+)(?:/status/(?P<status>\d+))?".format(domain)))
        nitters.append(re.compile(r"https?://{}/i/web/status/(?P<status>\d+).*".format(domain)))
    return nitters


@plugin.url_lazy(nitter_loader)
def nitter_to_twitter(bot, trigger):
    try:
        tweet = trigger.group("status")
        user = trigger.group("user")
        if tweet:
            twitter.output_status(bot, trigger, tweet)
        elif user:
            twitter.output_user(bot, trigger, user)
        else:
            return
    except BaseException:
        return
