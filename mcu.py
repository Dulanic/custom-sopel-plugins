"""
Original author: xnaas (2021-2022)
License: The Unlicense (public domain)
"""
import requests
from sopel import plugin
from sopel.formatting import bold, italic


@plugin.command("nextmcu")
@plugin.output_prefix("[MCU] ")
def next_mcu(bot, trigger):
    """Info on the next MCU release."""
    url = "https://whenisthenextmcufilm.com/api"
    try:
        r = requests.get(url)
        days_until = str(r.json()["days_until"])
        media_title = r.json()["title"]
        media_type = r.json()["type"]
        msg = f"Up next in the MCU is the {media_type} '{italic(media_title)}'. "
        msg += f"It will be out in {bold(days_until)} days."
        bot.say(msg)
    except BaseException:
        bot.reply("Error reaching API, probably.")


# TODO: This entire command is pretty fucked, tbh.
#   Needs to have shit put into a dict or something
#   and get some for loops going.
#   - xnaas, 2022
@plugin.command("next4mcu")
@plugin.output_prefix("[MCU] ")
def next4_mcu(bot, trigger):
    """Info on the next MCU release."""
    url = "https://whenisthenextmcufilm.com/api"
    try:
        # 1st Request
        r1 = requests.get(url)

        # 1st Next Item
        days_until_1 = str(r1.json()["days_until"])
        media_title_1 = r1.json()["title"]
        media_type_1 = r1.json()["type"]
        # 2nd Next Item
        days_until_2 = str(r1.json()["following_production"]["days_until"])
        media_title_2 = r1.json()["following_production"]["title"]
        media_type_2 = r1.json()["following_production"]["type"]
        release_date_2 = r1.json()["following_production"]["release_date"]

        # 2nd Request
        date_for_r2 = {"date": release_date_2}
        r2 = requests.get(url, params=date_for_r2)

        # 3rd Next Item
        days_until_3 = str(r2.json()["days_until"])
        media_title_3 = r2.json()["title"]
        media_type_3 = r2.json()["type"]
        # 4th Next Item
        days_until_4 = str(r2.json()["following_production"]["days_until"])
        media_title_4 = r2.json()["following_production"]["title"]
        media_type_4 = r2.json()["following_production"]["type"]

        bot.say("Here are the next 4 upcoming MCU items:")

        msg1 = f"Immediately up next is the {media_type_1} '{italic(media_title_1)}'. "
        msg1 += f"It will be out in {bold(days_until_1)} days."

        msg2 = f"After that will be the {media_type_2} '{italic(media_title_2)}'. "
        msg2 += f"It will be out in {bold(days_until_2)} days."

        msg3 = f"After that will be the {media_type_3} '{italic(media_title_3)}'. "
        msg3 += f"It will be out in {bold(days_until_3)} days."

        msg4 = f"Finally, after that is the {media_type_4} '{italic(media_title_4)}'. "
        msg4 += f"It will be out in {bold(days_until_4)} days."

        bot.say(msg1)
        bot.say(msg2)
        bot.say(msg3)
        bot.say(msg4)
    except BaseException:
        bot.reply("Error reaching API, probably.")
