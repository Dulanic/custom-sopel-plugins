"""
Original author: xnaas (2021)
License: The Unlicense (public domain)
"""
import base64
from sopel import plugin


@plugin.command('b64e')
@plugin.example('.b64e I love you.')
@plugin.output_prefix('[Base64] ')
def base64_encode(bot, trigger):
    """Encodes a message into base64."""
    if not trigger.group(2):
        return bot.reply('I need something to encode.')

    encodedBytes = base64.b64encode(trigger.group(2).encode('utf-8'))
    encodedStr = str(encodedBytes, 'utf-8')

    bot.say(encodedStr)


@plugin.command('b64d')
@plugin.example('.b64d V293ISBNdWNoIHNlY3JldC4=')
@plugin.output_prefix('[Base64] ')
def base64_decode(bot, trigger):
    """Decodes a base64 string."""
    if not trigger.group(2):
        return bot.reply('I need something to decode.')

    try:
        decodedBytes = base64.b64decode(trigger.group(2).encode('utf-8'))
        decodedStr = str(decodedBytes, 'utf-8')
        bot.say(decodedStr)
    except Exception:
        bot.reply('I need real base64, fool.')
