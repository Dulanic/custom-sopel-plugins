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

    q = r["result"][0]
    marketState = q["marketState"]
    quoteType = q["quoteType"]

    if quoteType == "EQUITY" and marketState == "PRE":
        data = {
            "price": q["preMarketPrice"],
            "change": q["preMarketChange"],
            "percentchange": q["preMarketChangePercent"],
            "low": q["regularMarketDayLow"],
            "high": q["regularMarketDayHigh"],
            "cap": int_to_human(q["marketCap"]),
            "name": q["longName"],
            "close": q["regularMarketPreviousClose"],
            "currencySymbol": cur_to_symbol(q["currency"]),
            "marketState": marketState
        }
    elif quoteType == "EQUITY" and marketState == "REGULAR":
        data = {
            "price": q["regularMarketPrice"],
            "change": q["regularMarketChange"],
            "percentchange": q["regularMarketChangePercent"],
            "low": q["regularMarketDayLow"],
            "high": q["regularMarketDayHigh"],
            "cap": int_to_human(q["marketCap"]),
            "name": q["longName"],
            "close": q["regularMarketPreviousClose"],
            "currencySymbol": cur_to_symbol(q["currency"]),
            "marketState": marketState
        }
    elif quoteType == "EQUITY" and ((marketState == "POST" or marketState == "POSTPOST") and "postMarketPrice" in q):
        data = {
            "price": q["postMarketPrice"],
            "change": q["postMarketChange"],
            "percentchange": q["postMarketChangePercent"],
            "low": q["regularMarketDayLow"],
            "high": q["regularMarketDayHigh"],
            "cap": int_to_human(q["marketCap"]),
            "name": q["longName"],
            "close": q["regularMarketPreviousClose"],
            "rmchange": q["regularMarketChange"],
            "rmpercentchange": q["regularMarketChangePercent"],
            "currencySymbol": cur_to_symbol(q["currency"]),
            "marketState": marketState
        }
    elif quoteType == "FUTURE":
        # TODO: more data
        data = {"price": q["regularMarketPrice"]}
    else:
        return bot.say(
            "[DEBUG] Unsupported or other issue. Type: {}, State: {}".format(
                quoteType, marketState))

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

    r = r["result"]

    # might not need this?
    data = {}
    data.clear()

    # TODO: import more data, better:
    # for Quote in Results
    for q in r:
        marketState = q["marketState"]
        if marketState == "PRE":
            data.update({
                "{}".format(q["symbol"]): "{}".format(q["regularMarketPrice"])
            })
        elif marketState == "REGULAR":
            data.update({
                "{}".format(q["symbol"]): "{}".format(q["regularMarketPrice"])
            })
        elif marketState == "POST" or marketState == "POSTPOST":
            data.update({
                "{}".format(q["symbol"]): "{}".format(q["regularMarketPrice"])
            })
        else:
            return bot.say(
                "[DEBUG] Error: Unknown market state: {}".format(marketState))

    return data


def int_to_human(n):
    # If a stock hits a quadrillion dollar value...jesus.
    if n >= 1e15:
        return "Holy shit!"
    # Trillions
    elif n >= 1e12:
        n = str(round(n / 1e12, 2))
        return n + "T"
    # Billions
    elif n >= 1e9:
        n = str(round(n / 1e9, 2))
        return n + "B"
    # Millions
    elif n >= 1e6:
        n = str(round(n / 1e6, 2))
        return n + "M"
    # Shouldn't be anything lower than millions, but...
    return str(n)


def cur_to_symbol(currency):
    # not exhaustive
    currencies = {
        "USD": "$",
        "CAD": "C$",
        "JPY": "JP¥",
        "CNY": "CN¥",
        "EUR": "€"
    }
    # default to $
    if currency not in currencies:
        cs = "$"
    else:
        cs = currencies[currency]
    return cs


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
    price = data["price"]
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
    try:
        data = data.items()
    except AttributeError:
        return bot.say("[DEBUG] No dict to output.")
    return bot.say("[DEBUG] {}".format(data))

    # price = data["result"][0]["regularMarketPrice"]
    # ticker = data["result"][0]["symbol"]
    # bot.say("{}: ${:.2f}".format(ticker, price))
