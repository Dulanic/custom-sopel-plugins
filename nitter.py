"""
Original author: xnaas
License: Eiffel Forum License, version 2
Note: some regex stolen from https://github.com/sopel-irc/sopel-twitter
"""
from sopel import plugin
from sopel_modules import twitter
import re


NITTER_DOMAINS = [
    "nitter.net",
    "nitter.42l.fr",
    "nitter.pussthecat.org",
    "nitter.nixnet.services",
    "nitter.fdn.fr",
    "nitter.1d4.us",
    "nitter.kavin.rocks",
    "nitter.unixfox.eu",
    "nitter.domain.glass",
    "nitter.eu",
    "nitter.namazso.eu",
    "nitter.actionsack.com",
    "birdsite.xanny.family",
    "nitter.hu",
    "twitr.gq",
    "nitter.moomoo.me",
    "nittereu.moomoo.me",
    "bird.trom.tf",
    "nitter.it",
    "twitter.censors.us",
    "nitter.grimneko.de",
    "nitter.alefvanoon.xyz",
    "n.hyperborea.cloud",
    "nitter.ca",
    "twitter.076.ne.jp",
    "nitter.mstdn.social",
    "nitter.fly.dev",
    "notabird.site",
    "nitter.weiler.rocks",
    "nitter.silkky.cloud",
    "nitter.sethforprivacy.com",
    "nttr.stream",
    "nitter.cutelab.space",
    "nitter.nl",
    "nitter.mint.lgbt",
    "nitter.bus-hit.me",
    "fuckthesacklers.network",
    "nitter.govt.land",
    "nitter.datatunnel.xyz",
    "nitter.esmailelbob.xyz",
    "tw.artemislena.eu",
    "de.nttr.stream",
    "nitter.winscloud.net",
    "nitter.tiekoetter.com",
    "nitter.spaceint.fr",
    "twtr.bch.bar",
    "nitter.privacy.com.de",
    "nitter.mastodon.pro",
    "nitter.notraxx.ch",
    "nitter.poast.org",
    "nitter.lunar.icu",
    "nitter.bird.froth.zone"
]


def nitter_loader(settings):
    nitters = []
    for domain in NITTER_DOMAINS:
        nitters.append(re.compile(r"https?://{}/(?P<user>\w+)(?:/status/(?P<status>\d+))?".format(re.escape(domain))))
        nitters.append(re.compile(r"https?://{}/i/web/status/(?P<status>\d+).*".format(re.escape(domain))))
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
