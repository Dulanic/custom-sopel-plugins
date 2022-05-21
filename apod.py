"""
Authors: xnaas (2022)
License: The Unlicense (public domain)
"""
import re
import requests
from sopel import plugin
from sopel.formatting import plain


VALID_APOD = r'https?://apod\.nasa\.gov/apod/(?P<date>ap\d{6}|astropix)\.html'
API_URL = 'https://api.nasa.gov/planetary/apod'


def apod_loader(settings):
    return [re.compile(VALID_APOD)]


def get_apod_api_key(bot):
    apikey = bot.db.get_plugin_value('apod', 'api_key', None)
    if not apikey:
        msg =  'You must set an API key with `.apodkey <key_here>` '
        msg += 'You can get a key from: https://api.nasa.gov'
        raise Exception(msg)
    return apikey


def get_apod_data(params, trigger):
    try:
        r = requests.get(API_URL, params=params)
    except Exception as e:
        raise Exception(e)

    if r.status_code != 200:
        http_error_msg = f'HTTP Error: {r.status_code}'
        if r.status_code == 400:
            http_error_msg = f'Bad Request: no APOD for this day, most likely'
        if r.status_code == 403:
            http_error_msg = 'invalid or missing API key'
        raise Exception(http_error_msg)

    media_type = r.json()['media_type']
    if media_type == 'image':
        link = r.json()['hdurl']
    elif media_type == 'video':
        link = r.json()['url']
    else:
        raise Exception(f'unhandled media type: {media_type} | url: {trigger.group(0)}')
    title = r.json()['title']
    info = r.json()['explanation'].replace('  ', ' ')  # replace double space with single
    return info, link, title


@plugin.command('apod')
@plugin.output_prefix('[APOD] ')
def apod_cmd(bot, trigger):
    """Get the latest APOD image/info."""
    try:
        apikey = get_apod_api_key(bot)
    except Exception as e:
        bot.say(str(e))

    params = {'api_key': apikey}
    try:
        info, link, title = get_apod_data(params, trigger)
    except Exception as e:
        bot.say(str(e))

    bot.say(f'{title} | {link} | {info}', truncation=' […]')


@plugin.output_prefix('[APOD] ')
@plugin.url_lazy(apod_loader)
def apod_from_url(bot, trigger):
    try:
        apikey = get_apod_api_key(bot)
    except Exception as e:
        bot.say(str(e))

    date = trigger.group('date')
    if date == 'astropix':
        params = {'api_key': apikey}
    else:
        YY = int(date[2:4])
        MM = int(date[4:6])
        DD = int(date[6:8])
        # What is NASA's plan for year 2095 and beyond?
        # Why does NASA hate everything and use 2-digit years in their URLs?
        if 95 <= YY <= 99:
            date = f'19{YY}-{MM}-{DD}'
        elif 00 <= YY <= 94:
            date = f'20{YY}-{MM}-{DD}'
        else:
            return bot.say('ERROR: invalid date: {date}')
        params = {'api_key': apikey, 'date': date}

    try:
        info, link, title = get_apod_data(params, trigger)
    except Exception as e:
        return bot.say(str(e))

    bot.say(f'{title} | {link} | {info}', truncation=' […]')


@plugin.command('apodkey')
@plugin.example('.apodkey abc123')
@plugin.require_admin
@plugin.require_privmsg
def apod_set_key(bot, trigger):
    """DM the bot your NASA API key for use with APOD stuff."""
    apikey = plain(trigger.group(3) or '')
    if not apikey:
        return bot.say('You need to supply an API key.')
    bot.db.set_plugin_value('apod', 'api_key', apikey)
    bot.say(f'API key set as: {apikey}')
