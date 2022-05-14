"""
Authors: dgw (2020-2021), xnaas (2020-2022)
Fork: https://github.com/xnaas/sopel-color-text
Source: https://github.com/sopel-irc/sopel-rainbow
License: Eiffel Forum License, version 2
"""
import itertools
import unicodedata
from sopel import plugin
from sopel.formatting import color, plain


COLOR_SCHEMES = {
    'rainbow': [4, 7, 8, 3, 12, 2, 6],
    'usa': [4, 0, 2],
    'commie': [4, 8],
    'spooky': [8, 7, 0],
}
SCHEME_ERRORS = {
    'rainbow': "I can't make a rainbow out of nothing!",
    'usa': "I can't distribute FREEDOM out of nothing!",
    'commie': "I need text to commie-ize!",
    'spooky': "I need text to spookify!",
}


@plugin.commands('rainbow', 'usa', 'commie', 'spooky')
def rainbow_cmd(bot, trigger):
    """Make text colored. Options are 'rainbow', 'usa', 'commie', and 'spooky'."""
    text = plain(trigger.group(2) or '')
    scheme = trigger.group(1).lower()

    if not text:
        return bot.reply(SCHEME_ERRORS[scheme])

    try:
        colors = COLOR_SCHEMES[scheme]
    except KeyError:
        # not possible to reach this at time of writing, but who knows?
        # mistakes happen when updating stuff that needs to be changed in
        # parallel
        return bot.reply(
            f"I don't know what color sequence to use for '{scheme}'!")

    color_cycle = itertools.cycle(colors)

    bot.say(
        ''.join(
            char if unicodedata.category(char) == 'Zs'
            else color(char, next(color_cycle))
            for char in text
        ), max_messages=4
    )
