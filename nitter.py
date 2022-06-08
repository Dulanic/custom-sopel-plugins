"""
Author: xnaas (2022)
License: Eiffel Forum License, version 2
Note: some regex stolen from https://github.com/sopel-irc/sopel-twitter
"""
import re
from sopel import plugin
from sopel_modules import twitter


NITTER_DOMAINS = [
    'n.actionsack.com',
    'nitter.net',
    'nitter.42l.fr',
    'nitter.pussthecat.org',
    'nitter.nixnet.services',
    'nitter.fdn.fr',
    'nitter.1d4.us',
    'nitter.kavin.rocks',
    'nitter.unixfox.eu',
    'nitter.domain.glass',
    'nitter.namazso.eu',
    'birdsite.xanny.family',
    'nitter.hu',
    'nitter.moomoo.me',
    'nittereu.moomoo.me',
    'bird.trom.tf',
    'nitter.it',
    'twitter.censors.us',
    'nitter.grimneko.de',
    'n.hyperborea.cloud',
    'nitter.ca',
    'twitter.076.ne.jp',
    'nitter.mstdn.social',
    'nitter.fly.dev',
    'notabird.site',
    'nitter.weiler.rocks',
    'nitter.silkky.cloud',
    'nitter.sethforprivacy.com',
    'nttr.stream',
    'nitter.cutelab.space',
    'nitter.nl',
    'nitter.mint.lgbt',
    'nitter.bus-hit.me',
    'fuckthesacklers.network',
    'nitter.govt.land',
    'nitter.esmailelbob.xyz',
    'tw.artemislena.eu',
    'de.nttr.stream',
    'nitter.winscloud.net',
    'nitter.tiekoetter.com',
    'nitter.spaceint.fr',
    'twtr.bch.bar',
    'nitter.privacy.com.de',
    'nitter.mastodon.pro',
    'nitter.notraxx.ch',
    'nitter.poast.org',
    'nitter.lunar.icu',
    'nitter.bird.froth.zone',
    'nitter.dcs0.hu',
    'twitter.dr460nf1r3.org',
    'twitter.beparanoid.de',
    'n.ramle.be'
]


def nitter_loader(settings):
    nitters = []
    for domain in NITTER_DOMAINS:
        nitters.append(re.compile(fr"https?://{re.escape(domain)}/(?P<user>\w+)(?:/status/(?P<status>\d+))?"))
        nitters.append(re.compile(fr"https?://{re.escape(domain)}/i/web/status/(?P<status>\d+).*"))
    return nitters


@plugin.url_lazy(nitter_loader)
def nitter_to_twitter(bot, trigger):
    try:
        tweet = trigger.group('status')
        user = trigger.group('user')
        if tweet:
            twitter.output_status(bot, trigger, tweet)
        elif user:
            if user in ['pic', 'search']:
                return
            twitter.output_user(bot, trigger, user)
        else:
            return
    except BaseException:
        return
