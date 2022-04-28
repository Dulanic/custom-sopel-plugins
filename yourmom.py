"""
Original author: xnaas
License: The Unlicense (public domain)
"""
from secrets import choice as choose
from sopel import plugin
import os


@plugin.command("ym")
def yourmom(bot, trigger):
    file = os.path.join(os.path.dirname(__file__), "yourmom.txt")
    joke = choose(open(file).readlines())
    bot.say(joke)
