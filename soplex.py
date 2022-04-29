"""
Original author: xnaas (2021)
License: The Unlicense (public domain)
"""
import plexapi.exceptions
import requests.exceptions
from plexapi.server import PlexServer
from sopel import config, formatting, plugin
from sopel.config.types import StaticSection, ValidatedAttribute


# Define Config Options
class PlexSection(StaticSection):
    baseurl = ValidatedAttribute("baseurl", str)
    token = ValidatedAttribute("token", str)


def setup(bot):
    bot.config.define_section("plex", PlexSection)


def configure(config):
    config.define_section("plex", PlexSection)
    config.plex.configure_setting("baseurl", "http://yourplexserver:32400")
    config.plex.configure_setting("token", "your Plex token")


# Verifies connection and sets 'plex' value
def plex_test(bot, trigger):
    try:
        baseurl = bot.config.plex.baseurl
        token = bot.config.plex.token
        plex = PlexServer(baseurl, token)
        return plex
    except requests.exceptions.ConnectionError:
        bot.reply("Plex server unreachable.")
    except plexapi.exceptions.Unauthorized:
        bot.reply("Bad Plex token configured.")


@plugin.command("plextest", "testplex")
@plugin.require_admin
def plex_test_cmd(bot, trigger):
    """Test if your configured options can reach Plex."""
    plex = plex_test(bot, trigger)

    if plex is None:
        return
    else:
        bot.reply("Plex connection test successful.")


@plugin.command("prm")
def plex_recentmovies(bot, trigger):
    """List the 3 most recently added movies."""
    plex = plex_test(bot, trigger)

    if plex is None:
        return

    movies = plex.library.section("Movies")
    recent = movies.recentlyAdded(maxresults=3)
    recent_movies = []
    for movie in recent:
        recent_movies.append("{} ({})".format(movie.title, movie.year))

    bot.reply(", ".join(recent_movies))


@plugin.command("plexsearch", "searchplex")
def plex_search(bot, trigger):
    """Search Plex for a movie or show."""
    search = formatting.plain(trigger.group(2) or '')

    if not search:
        try:
            msg = "I need something to search..."
        except KeyError:
            msg = "How did you do that?!"
        bot.reply(msg)
        return

    plex = plex_test(bot, trigger)

    if plex is None:
        return

    search_results = []

    # Search and add Movies to search_results
    for video in plex.search(search, mediatype="movie", limit=3):
        search_results.append(
            "[{}] {} ({})".format(
                video.TYPE.title(),
                video.title,
                video.year))

    # Search and add TV Shows to search_results
    for video in plex.search(search, mediatype="show", limit=3):
        search_results.append(
            "[{}] {} ({})".format(
                video.TYPE.title(),
                video.title,
                video.year))

    # verify there's results
    if not search_results:
        bot.reply("No results for your query.")
    else:
        bot.reply(", ".join(search_results))
