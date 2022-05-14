"""
Original author: xnaas (2020, 2022)
License: The Unlicense (public domain)
"""
import requests
from sopel import plugin


@plugin.commands('catgif', 'cat')
def cats(bot, trigger):
    cmd = trigger.group(1).lower()
    url = 'https://api.thecatapi.com/v1/images/search'
    if cmd == 'cat':
        param = {'mime_types': 'jpg,png'}
    elif cmd == 'catgif':
        param = {'mime_types': 'gif'}
    try:
        cat_img = requests.get(url, params=param).json()[0]['url']
        bot.say(cat_img)
    except Exception:
        bot.reply('Error reaching API, probably.')


@plugin.command('catfact')
def catfact(bot, trigger):
    url = 'https://cat-fact.herokuapp.com/facts/random'
    params = {'animal_type': 'cat', 'amount': '1'}
    try:
        cat_fact = requests.get(url, params=params).json()['text']
        bot.say(cat_fact)
    except Exception:
        bot.reply('Error reaching API, probably.')


@plugin.command('dog')
def dogs(bot, trigger):
    url = 'https://dog.ceo/api/breeds/image/random'
    try:
        dog_image = requests.get(url).json()['message']
        bot.say(dog_image)
    except Exception:
        bot.reply('Error reaching API, probably.')


@plugin.command('dogfact')
def dogfact(bot, trigger):
    url = 'https://dog-facts-api.herokuapp.com/api/v1/resources/dogs'
    params = {'number': '1'}
    try:
        dog_fact = requests.get(url, params=params).json()[0]['fact']
        bot.say(dog_fact)
    except Exception:
        bot.reply('Error reaching API, probably.')


@plugin.commands('shibe', 'bir(b|d)')
def shibe_api(bot, trigger):
    cmd = trigger.group(1).lower()
    base_url = 'https://shibe.online/api'
    params = {'count': '1', 'urls': 'true', 'httpsUrls': 'true'}

    if cmd == 'shibe':
        url = f'{base_url}shibes'
    elif cmd in {'birb', 'bird'}:
        url = f'{base_url}birds'

    try:
        img = requests.get(url, params=params).json()[0]
        bot.say(img)
    except Exception:
        bot.reply('Error reaching API, probably.')


@plugin.commands('fox(|y)')
def foxes(bot, trigger):
    url = 'https://randomfox.ca/floof'
    try:
        fox_image = requests.get(url).json()['image']
        bot.say(fox_image)
    except Exception:
        bot.reply('Error reaching API, probably.')
