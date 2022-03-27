from bs4 import BeautifulSoup
from sopel import plugin
from sopel.formatting import bold, italic, plain
import requests


PCOUNT_URL = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1"
SEARCH_URL = "https://store.steampowered.com/search/suggest"


@plugin.commands("steam pcount", "steam players", "steam search", "steam store", "steam")
@plugin.output_prefix("[Steam] ")
def steam_base(bot, trigger):
    cmd = trigger.group(1).lower()

    search_terms = plain(trigger.group(2) or '')
    if not search_terms:
        return bot.reply("I need something to lookup, dummy!")

    msg, appid, app_name, app_price, app_url = steam_search(search_terms)
    if msg:
        return bot.say(msg)

    if cmd == "steam pcount" or cmd == "steam players":
        msg = steam_pcount(appid, app_name)
    elif cmd == "steam search" or cmd == "steam store" or cmd == "steam":
        msg = "{} ({})".format(app_url, app_price)

    bot.say(msg)


def steam_pcount(appid, app_name, msg=None):
    param = {"appid": appid}
    try:
        pcount = requests.get(PCOUNT_URL, params=param).json()["response"]["player_count"]
    except requests.exceptions.ConnectionError:
        msg = "Error reaching Steam Web API."
    except AttributeError:
        msg = "Invalid AppID somehow...good luck fixing this one, xnaas!"
    except KeyError:
        msg = "No player count data for {}.".format(bold(app_name))

    if msg:
        return msg

    # configure and send player count
    pcount = "{:,}".format(pcount)
    msg = "There are currently {} people playing {}.".format(bold(pcount), italic(app_name))
    return msg


def steam_search(search_terms):
    # init everything as None
    msg = appid = app_name = app_price = app_url = None

    # ISSUE: only supports US English searches
    params = {
        "term": search_terms,
        "f": "games",
        "cc": "US",
        "realm": 1,
        "l": "english",
        "use_store_query": 1
    }

    try:
        r = requests.get(SEARCH_URL, params=params)
    except requests.exceptions.ConnectionError:
        msg = "Error reaching Steam Web API."
        return msg, appid, app_name, app_price, app_url

    html = BeautifulSoup(r.text, "html.parser")
    try:
        appid = html.select_one("a.match:nth-child(1)").attrs["data-ds-appid"]
        app_name = html.select_one("a.match:nth-child(1) > div:nth-child(1)").string
        app_price = html.select_one("a.match:nth-child(1) > div:nth-child(3)").string
        app_url = html.select_one("a.match:nth-child(1)").attrs["href"].split("?")[0]
    except AttributeError:
        msg = "No results for {}".format(bold(search_terms))
        return msg, appid, app_name, app_price, app_url

    return msg, appid, app_name, app_price, app_url
