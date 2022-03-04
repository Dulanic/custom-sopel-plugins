from sopel import plugin
# from sopel import config, plugin
# from sopel.config.types import StaticSection, ValidatedAttribute
import re  # to be used Later™
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
YHEAD = {"User-Agent": "actionsack.com"}


@plugin.command("oil")
@plugin.output_prefix("[OIL] ")
# @plugin.require_chanmsg
def yf_oil(bot, trigger):
    """Get the latest Brent Crude Oil price per barrel."""
    PARAMS = {"symbols": "BZ=F"}

    try:
        data = requests.get(url=URL, params=PARAMS, headers=YHEAD).json()["quoteResponse"]["result"][0]
        price = data["regularMarketPrice"]
        # TODO: Additional data points
    except requests.exceptions.RequestException:
        return bot.reply("Issue with API.")
    except KeyError:
        return bot.reply("Issue with API.")

    bot.say("PPB: ${:.2f}".format(price))
