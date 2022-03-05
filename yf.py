from sopel import plugin
# from sopel import config, plugin
# from sopel.config.types import StaticSection, ValidatedAttribute
import re
import requests


# Unused config section at the moment.
# Yahoo Finance has no API key, but...
# there might be something we want to
# configure in the future? ¯\_(ツ)_/¯
# class YFSection(StaticSection):
#     api_key = ValidatedAttribute("api_key", str)
#
#
# def setup(bot):
#     bot.config.define_section("yf", YFSection)
#
#
# def configure(config):
#     config.define_section("yf", YFSection)
#     config.yf.configure_setting("api_key", "some YF config option")


URL = "https://query1.finance.yahoo.com/v7/finance/quote"
# Yahoo ignores the default python requests ua
YHEAD = {"User-Agent": "thx 4 the API <3"}


def get_quote(bot, symbol):
    try:
        r = requests.get(url=URL, params=symbol, headers=YHEAD)
    except requests.exceptions.ConnectionError:
        raise Exception("Unable to reach Yahoo Finance.")

    if r.status_code != 200:
        raise Exception("HTTP Error {}".format(r.status_code))

    r = r.json()["quoteResponse"]

    if not r["result"]:
        raise Exception("No data found. Input data likely bad.")

    # probably not necessary:
    data = {}
    data.clear()

    # TODO: dict with lots of data
    data = {"price": "{}".format(r["result"][0]["regularMarketPrice"])}

    return data


def get_quote_multi(bot, symbols):
    try:
        r = requests.get(url=URL, params=symbols, headers=YHEAD)
    except requests.exceptions.ConnectionError:
        raise Exception("Unable to reach Yahoo Finance.")

    if r.status_code != 200:
        raise Exception("HTTP Error {}".format(r.status_code))

    r = r.json()["quoteResponse"]

    if not r["result"]:
        raise Exception("No data found. Input data likely bad.")

    # probably not necessary:
    data = {}
    data.clear()

    # TODO: import more data, better:
    for q in r["result"]:
        data.update({"{}".format(q["symbol"]): "{}".format(q["regularMarketPrice"])})

    return data


@plugin.command("oil")
@plugin.output_prefix("[OIL] ")
def yf_oil(bot, trigger):
    """Get the latest Brent Crude Oil price per barrel."""
    # hardcode "Brent Crude Oil Last Day Financ"
    symbol = {"symbols": "BZ=F"}

    try:
        data = get_quote(bot, symbol)
    except Exception as e:
        return bot.say(str(e))

    # TODO: Additional data points
    price = data
    bot.say("PPB: ${:.2f}".format(price))


@plugin.command("stockb")
@plugin.output_prefix("[STOCKS BETA] ")
def yf_stock(bot, trigger):
    """Get stock(s) info."""
    if not trigger.group(2):
        return bot.reply("I need a (list of) stock ticker(s).")

    symbols = trigger.group(2).upper()

    if re.search(",", symbols):
        symbols = {"symbols": symbols}
        try:
            data = get_quote_multi(bot, symbols)
        except Exception as e:
            return bot.say(str(e))
    else:
        symbol = {"symbols": symbols}
        try:
            data = get_quote(bot, symbol)
        except Exception as e:
            return bot.say(str(e))

    # DEBUG
    data = data.items()
    bot.say("[DEBUG] {}".format(data))
    return

    # price = data["result"][0]["regularMarketPrice"]
    # ticker = data["result"][0]["symbol"]
    # bot.say("{}: ${:.2f}".format(ticker, price))
