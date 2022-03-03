from sopel import config, plugin
from sopel.config.types import StaticSection, ValidatedAttribute
# import re
import requests


class CommoditiesSection(StaticSection):
    api_key = ValidatedAttribute("api_key", str)


def setup(bot):
    bot.config.define_section("commodities", CommoditiesSection)


def configure(config):
    config.define_section("commodities", CommoditiesSection)
    config.commodities.configure_setting("api_key", "commodities api key")


BASE_URL = "https://commodities-api.com/api/latest"


@plugin.commands("oil")
@plugin.output_prefix("[OIL] ")
def commodities_oil(bot, trigger):
    # TODO: config all the things, obviously
    PARAMS = {
        "access_key": bot.config.commodities.api_key,
        "base": "BRENTOIL",
        "symbols": "USD,CAD,EUR"
    }

    try:
        rates = requests.get(url=BASE_URL, params=PARAMS).json()["data"]["rates"]
        CAD = round(rates["CAD"], 2)
        EUR = round(rates["EUR"], 2)
        USD = round(rates["USD"], 2)
    except requests.exceptions.RequestException:
        return bot.reply("Issue with API.")
    except KeyError:
        return bot.reply("API key missing, most likely.")

    bot.say("PPB: ${} (€{}, C${})".format(USD, EUR, CAD))
