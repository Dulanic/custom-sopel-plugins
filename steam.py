"""
Original author: xnaas (2022)
License: The Unlicense (public domain)
"""
import requests
from bs4 import BeautifulSoup
from sopel import plugin
from sopel.formatting import bold, italic, plain


PCOUNT_URL = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1'
SEARCH_URL = 'https://store.steampowered.com/search/suggest'
OVERRIDES = {
    'drg': 'Deep Rock Galactic',
    'mcc': 'Halo: The Master Chief Collection',
    'space engine': 'SpaceEngine',
    'spaceengine': 'SpaceEngine'
}


@plugin.command('steam')
@plugin.rate(server=2)
def steam(bot, trigger):

    search_terms = plain(trigger.group(2) or '').lower()
    if not search_terms:
        bot.reply('I need something to lookup, dummy!')
        return plugin.NOLIMIT

    if search_terms in OVERRIDES:
        search_terms = OVERRIDES[search_terms]

    # ISSUE: only supports US English searches
    #   make configurable? ¯\_(ツ)_/¯
    search_params = {
        'term': search_terms,
        'f': 'games',
        'cc': 'US',
        'realm': 1,
        'l': 'english',
        'use_store_query': 1
    }

    # get app id, name, price, and url
    try:
        r = requests.get(SEARCH_URL, params=search_params)
    except requests.exceptions.ConnectionError:
        return bot.reply('Error reaching Steam Web API.')

    html = BeautifulSoup(r.text, 'html.parser')
    try:
        appid = html.select_one('a.match:nth-child(1)').attrs['data-ds-appid']
        app_name = html.select_one('a.match:nth-child(1) > div:nth-child(1)').string
        app_price = html.select_one('a.match:nth-child(1) > div:nth-child(3)').string
        app_url = html.select_one('a.match:nth-child(1)').attrs['href'].split('?')[0]
    except AttributeError:
        return bot.reply(f'No results for {bold(search_terms)}')

    if not app_price:
        app_price = '$?'

    # get player count
    pcount_param = {'appid': appid}
    try:
        pcount = requests.get(PCOUNT_URL, params=pcount_param).json()['response']['player_count']
        pcount = f'{pcount:,}'
    except requests.exceptions.ConnectionError:
        return bot.reply('Error reaching Steam Web API.')
    except AttributeError:
        return bot.say(f'Steam: Invalid AppID ({bold(appid)}) somehow...gl xnaas!')
    except KeyError:
        pcount = '?'

    app_url = app_url.rsplit('/', maxsplit=1)[:1][0][8:]  # trim app URL

    # finally: send message
    bot.say(f'{app_name}: {bold(app_price)} ({pcount} players) | {app_url}')
