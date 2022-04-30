"""
Original author: xnaas (2021-2022)
License: The Unlicense (public domain)
"""
import random
from sopel import plugin, tools
from sopel.formatting import plain


@plugin.command("penis")
@plugin.require_chanmsg
def literal_dick_measuring(bot, trigger):
    """100% accurate penis measuring."""
    target = plain(trigger.group(3) or trigger.nick)

    if not target:
        return bot.reply("How in the hell did you do this?")

    # Set Case Insensitivity
    target = tools.Identifier(target)

    # Lock in the random state
    state = random.getstate()

    # Check user is in channel
    if target not in bot.channels[trigger.sender].users:
        return bot.reply("I need someone in chat to measure. ( ͡° ͜ʖ ͡°)")

    # Get dick length
    if target == bot.nick:
        length = 20
    else:
        random.seed(str(target).lower())
        length = random.randint(0, 10)

    dick_length = f"8{'=' * length}D"

    # Restore random state
    random.setstate(state)

    # Tell user their dick length
    bot.say(f"{target}'s dick size: {dick_length}")
