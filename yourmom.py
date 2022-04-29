"""
Original author: xnaas (2021)
License: The Unlicense (public domain)
"""
import os
from secrets import choice as choose
from sopel import plugin


@plugin.command("ym")
def yourmom(bot, trigger):
    file = os.path.join(os.path.dirname(__file__), "yourmom.txt")
    joke = choose(open(file).readlines())
    bot.say(joke)
