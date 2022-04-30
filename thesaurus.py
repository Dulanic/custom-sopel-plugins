"""
Original author: xnaas (2022)
License: The Unlicense (public domain)
"""
import requests
from sopel import plugin, formatting
from sopel.config.types import StaticSection, ValidatedAttribute


class ThesaurusSection(StaticSection):
    api_key = ValidatedAttribute("api_key", str)


def setup(bot):
    bot.config.define_section("thesaurus", ThesaurusSection)


def configure(config):
    config.define_section("thesaurus", ThesaurusSection)
    config.thesaurus.configure_setting("api_key", "dictionaryapi.com api key")


@plugin.command("syn", "synonym")
@plugin.output_prefix("[synonym] ")
def synonyms(bot, trigger):
    word = formatting.plain(trigger.group(3))

    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}"
    key = {"key": bot.config.thesaurus.api_key}

    try:
        synonyms = requests.get(url, params=key).json()[0]["meta"]["syns"][0]
        bot.say(", ".join(synonyms), max_messages=2)
    except IndexError:
        bot.reply("No results.")


@plugin.command("ant", "antonym")
@plugin.output_prefix("[antonym] ")
def antonyms(bot, trigger):
    word = formatting.plain(trigger.group(3))

    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}"
    key = {"key": bot.config.thesaurus.api_key}

    try:
        antonyms = requests.get(url, params=key).json()[0]["meta"]["ants"][0]
        bot.say(", ".join(antonyms), max_messages=2)
    except IndexError:
        bot.reply("No results.")
