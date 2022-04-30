"""
Original author: xnaas (2021-2022)
License: The Unlicense (public domain)
"""
import re
import requests
from sopel import plugin


@plugin.command("isbn")
def isbn(bot, trigger):
    """Look up a book by its ISBN."""
    if not re.match(
        r"((978[\--– ])?[0-9][0-9\--– ]{10}[\--– ][0-9xX])|((978)?[0-9]{9}[0-9Xx])",
            trigger.group(2)):
        return bot.reply("I need a valid ISBN.")

    isbn_sanitized = trigger.group(2).replace(" ", "").replace("-", "")
    url = f"https://openlibrary.org/isbn/{isbn_sanitized}"
    try:
        book = requests.get(url).url
        bot.say(book)
    except:
        bot.reply("Error reaching API, probably.")
