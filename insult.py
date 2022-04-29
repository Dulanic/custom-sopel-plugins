"""
Original author: xnaas (2021)
License: The Unlicense (public domain)
"""
import html
import requests
from sopel import plugin, tools


@plugin.command("insult")
@plugin.require_chanmsg
def insult(bot, trigger):
    """Insults another user."""
    url = "https://evilinsult.com/generate_insult.php"
    params = {"lang": "en", "type": "json"}
    target = trigger.group(3)

    if not target:
        return bot.reply("I need someone to insult, dipshit.")
    target = tools.Identifier(target)

    if target == bot.nick:
        return bot.reply("Nice try, retard.")

    if target not in bot.channels[trigger.sender].users:
        return bot.reply("I need someone to insult, dipshit.")

    try:
        insult = requests.get(url, params=params).json()['insult']
        insult_escaped = html.unescape(insult)
        bot.say(f"{target}: {insult_escaped}")
    except:
        bot.reply("There was an error. Fuck you.")
