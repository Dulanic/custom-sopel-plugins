"""
Original author: xnaas (2020)
License: The Unlicense (public domain)
"""
import requests
from sopel import plugin


@plugin.commands("dadjoke", "dj")
def dadjoke(bot, trigger):
    """Posts a dad joke."""
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    try:
        dad_joke = requests.get(url, headers=headers).json()['joke']
        bot.say(dad_joke)
    except:
        bot.reply("Error reaching API, probably.")
