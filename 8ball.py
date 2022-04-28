"""
Original author: xnaas
License: The Unlicense (public domain)
"""
from secrets import choice as choose
from sopel import plugin


@plugin.commands('8', '8ball')
@plugin.example('.8 Am I gay?')
def eightball(bot, trigger):
    """The magic 8ball is all-knowing and 100% accurate."""
    if not trigger.group(2):
        return bot.say(f"I need something to foretell, {trigger.nick}!")

    messages = [
        # Positive Replies (10)
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes – definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        # Ambiguous Bullshit Replies (5)
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        # Negative Replies (5)
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    bot.reply(choose(messages))
