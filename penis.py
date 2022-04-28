"""
Original author: xnaas
License: The Unlicense (public domain)
"""
from sopel import plugin, tools
import random


@plugin.command("penis")
@plugin.require_chanmsg
def literal_dick_measuring(bot, trigger):
    """100% accurate penis measuring."""
    target = trigger.group(3) or trigger.nick

    if not target:
        bot.reply("How in the hell did you do this?")
        return

    # Set Case Insensitivity
    target = tools.Identifier(target)

    # Lock in the random state
    state = random.getstate()

    # Check user is in channel
    if target not in bot.channels[trigger.sender].users:
        bot.reply("I need someone in chat to measure. ( ͡° ͜ʖ ͡°)")
        return

    # Get dick length
    if target == bot.nick:
        length = 20
    else:
        random.seed(str(target).lower())
        length = random.randint(0, 10)

    dick_length = "8{}D".format("=" * length)

    # Restore random state
    random.setstate(state)

    # Tell user their dick length
    bot.say("{}'s dick size: {}".format(target, dick_length))
