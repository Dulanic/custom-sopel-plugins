"""
Original author: xnaas (2021-2022)
License: The Unlicense (public domain)
"""
import random
import requests
import string
import urllib.parse
from sopel import plugin, formatting


@plugin.rule(".*🤖.*")
@plugin.command("rbot")
def rbot(bot, trigger):
    """Posts a randomly generated bot.
    Can also be triggered with a 🤖 emoji anywhere in a message."""
    random_length = random.randrange(1, 512)
    random_string = ''.join(
        random.SystemRandom().choice(
            string.ascii_letters +
            string.digits +
            string.punctuation) for _ in range(random_length))
    string_urlsafe = urllib.parse.quote(random_string)
    url = "https://robohash.org/{}.png".format(string_urlsafe)
    try:
        image = requests.get(url)
        # API recently started to fail a lot... (2022-03-15)
        if image.status_code == 500:
            return bot.reply("API returned HTTP 500 Internal Server Error")
        filename = ''.join(
            random.SystemRandom().choice(
                string.ascii_letters +
                string.digits) for _ in range(5))
        with open("/mnt/media/websites/actionsack.com/tmp/rh_{}.png".format(filename), "wb") as file:
            file.write(image.content)
        bot.say("https://actionsack.com/tmp/rh_{}.png".format(filename))
    except BaseException:
        bot.reply("Error reaching API, probably.")


@plugin.command("fakeperson")
@plugin.rate(server=2)  # endpoint doesn't generate a new image more than once per second anyway
def fakeperson(bot, trigger):
    """Posts a not real person. 😱
    Uses thispersondoesnotexist.com"""
    url = "https://thispersondoesnotexist.com/image"
    try:
        image = requests.get(url)
        filename = ''.join(
            random.SystemRandom().choice(
                string.ascii_letters +
                string.digits) for _ in range(5))
        with open("/mnt/media/websites/actionsack.com/tmp/fp_{}.jpg".format(filename), "wb") as file:
            file.write(image.content)
        bot.say(
            "https://actionsack.com/tmp/fp_{}.jpg".format(filename))
    except BaseException:
        bot.reply("Error reaching API, probably.")


@plugin.command("advice")
def advice(bot, trigger):
    url = "https://api.adviceslip.com/advice"
    try:
        advice = requests.get(url).json()["slip"]["advice"]
        bot.reply(advice)
    except BaseException:
        bot.reply("Error reaching API, probably.")


@plugin.command("ron")
def ronswanson(bot, trigger):
    """Get a Ron Swanson quote."""
    url = "https://ron-swanson-quotes.herokuapp.com/v2/quotes"
    try:
        quote = requests.get(url).json()[0]
        bot.say("Ron Swanson says: {}".format(quote))
    except BaseException:
        bot.reply("Error reaching API, probably.")
