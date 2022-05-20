"""
Original author: xnaas (2021)
License: The Unlicense (public domain)
"""
from sopel import plugin
from sopel.formatting import bold


@plugin.search("ya['’]ll")
def yall(bot, trigger):
    bot.reply("It's {}, you fucking moron.".format(bold("y'all")))
