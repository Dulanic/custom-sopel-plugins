from sopel import plugin
from sopel.formatting import bold, color, colors
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
        data = {
            "price": q["regularMarketPrice"],
            "change": q["regularMarketChange"],
            "percentchange": q["regularMarketChangePercent"],
            "low": q["regularMarketDayLow"],
            "high": q["regularMarketDayHigh"],
            "cap": "N/A",
            "name": q["shortName"],
            "close": q["regularMarketPreviousClose"],
            "currencySymbol": cur_to_symbol(q["currency"]),
            "marketState": marketState
        }
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
        data[q["symbol"]] = {
            "price": q["regularMarketPrice"],
            "percentchange": q["regularMarketChangePercent"]
        }
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


# shout-out to MrTap for this one
def name_scrubber(name):
    p = re.compile(
        ',? (ltd|ltee|llc|corp(oration)?|inc(orporated)?|limited|plc)\\.?$',
        re.I)
    return p.sub('', name)


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

    symbols = trigger.group(3).upper()

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
    # try:
    #     data = data.items()
    # except AttributeError:
    #     return bot.say("[DEBUG] No dict to output.")
    # return bot.say("[DEBUG] {}".format(data))
    # bot.say("[DEBUG] {}".format(data))
    if not data:
        return

    # if multi-stock
    if "price" not in data:
        items = []
        for symbol, attr in data.items():
            if attr["percentchange"] >= 0:
                percentchange = color(
                    "{:+,.2f}%".format(attr["percentchange"]), colors.GREEN)
                items.append(
                    "{}: ${:,.2f} ({})".format(
                        symbol,
                        attr["price"],
                        percentchange))
            else:
                percentchange = color(
                    "{:+,.2f}%".format(attr["percentchange"]), colors.RED)
                items.append(
                    "{}: ${:,.2f} ({})".format(
                        symbol,
                        attr["price"],
                        percentchange))
        return bot.say(" | ".join(items))

    # cleanup symbol
    symbol = symbol["symbols"]
    # cleanup full name
    data["name"] = name_scrubber(data["name"])

    # set base msg
    msg = "{d[name]} ({symbol}) | {d[currencySymbol]}" + \
        bold("{d[price]:,.2f} ")

    # Change is None, usually on IPOs
    if not data["change"]:
        msg = msg.format(symbol=symbol, d=data)
    # Otherwise, check change vs previous day
    else:
        if data["change"] >= 0:
            msg += color("{d[change]:+,.2f} {d[percentchange]:+,.2f}%",
                         colors.GREEN)
        else:
            msg += color("{d[change]:+,.2f} {d[percentchange]:+,.2f}%", colors.RED)

        msg = msg.format(symbol=symbol, d=data)

    msg2 = ""
    marketState = data["marketState"]
    if marketState == "PRE":
        msg += color(" PREMARKET", colors.LIGHT_GREY)
        msg2 += " | CLOSE {d[currencySymbol]}{d[close]:,.2f} "
    elif marketState == "POST" or marketState == "POSTPOST":
        msg += color(" POSTMARKET", colors.LIGHT_GREY)
        msg2 += " | CLOSE {d[currencySymbol]}{d[close]:,.2f} "
        if data["rmchange"] >= 0:
            msg2 += color("{d[rmchange]:+,.2f} {d[rmpercentchange]:+,.2f}%", colors.GREEN)
        else:
            msg2 += color("{d[rmchange]:+,.2f} {d[rmpercentchange]:+,.2f}%", colors.RED)

    # add some more shit to the message
    msg2 += " | "
    msg2 += color("L {d[low]:,.2f}", colors.RED) + " "
    msg2 += color("H {d[high]:,.2f}", colors.GREEN)
    msg2 += " | Cap {d[currencySymbol]}{d[cap]}"

    # set final message
    msg = ("{msg}" + msg2).format(msg=msg, d=data)

    # finally, the bot says something!
    return bot.say(msg)
