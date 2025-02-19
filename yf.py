"""
Author: xnaas (2022)
License: MIT License
Note: originally based on https://github.com/sopel-irc/sopel-stocks
"""
import re
import requests
from sopel import plugin
from sopel.formatting import bold, color, colors


URL = 'https://query1.finance.yahoo.com/v7/finance/quote'
# Yahoo ignores the default python requests ua
YHEAD = {'User-Agent': 'thx 4 the API <3'}


def get_quote(bot, symbol):
    try:
        r = requests.get(url=URL, params=symbol, headers=YHEAD)
    except requests.exceptions.ConnectionError:
        raise Exception('Unable to reach Yahoo Finance.')

    if r.status_code != 200:
        raise Exception(f'HTTP Error {r.status_code}')

    r = r.json()['quoteResponse']

    if not r['result']:
        raise Exception(f'No data for {bold(symbol["symbols"])}.')

    q = r['result'][0]
    try:
        exchange = q['exchange']
    except KeyError:
        raise Exception(f'No data for {bold(symbol["symbols"])}.')
    marketState = q['marketState']
    quoteType = q['quoteType']

    if all((quoteType == 'EQUITY' and marketState == 'PRE',
            exchange in {'NMS', 'NYQ'})):
        data = {
            'price': q['preMarketPrice'],
            'change': q['preMarketChange'],
            'percentchange': q['preMarketChangePercent'],
            'low': q['regularMarketDayLow'],
            'high': q['regularMarketDayHigh'],
            'cap': int_to_human(q['marketCap']),
            'name': q['longName'],
            'close': q['regularMarketPreviousClose'],
            'currencySymbol': cur_to_symbol(q['currency']),
            'marketState': marketState,
            'symbol': q['symbol'],
            'exchange': q['exchange']
        }
        return data
    elif all((quoteType == 'EQUITY',
            marketState == 'POST' or marketState == 'POSTPOST',
            'postMarketPrice' in q,
            exchange == 'NMS' or exchange == 'NYQ')):
        data = {
            'price': q['postMarketPrice'],
            'change': q['postMarketChange'],
            'percentchange': q['postMarketChangePercent'],
            'low': q['regularMarketDayLow'],
            'high': q['regularMarketDayHigh'],
            'cap': int_to_human(q['marketCap']),
            'name': q['longName'],
            'close': q['regularMarketPrice'],
            'rmchange': q['regularMarketChange'],
            'rmpercentchange': q['regularMarketChangePercent'],
            'currencySymbol': cur_to_symbol(q['currency']),
            'marketState': marketState,
            'symbol': q['symbol'],
            'exchange': q['exchange']
        }
        return data
    elif quoteType in {'FUTURE', 'INDEX', 'CURRENCY', 'ETF'}:
        try:
            data = {
                'price': q['regularMarketPrice'],
                'change': q['regularMarketChange'],
                'percentchange': q['regularMarketChangePercent'],
                'low': q['regularMarketDayLow'],
                'high': q['regularMarketDayHigh'],
                'cap': 'N/A',
                'name': q['shortName'],
                'close': q['regularMarketPreviousClose'],
                'currencySymbol': cur_to_symbol(q['currency']),
                'marketState': marketState,
                'symbol': q['symbol'],
                'exchange': q['exchange']
            }
        except KeyError:
            raise Exception(f'No data for {bold(symbol["symbols"])}.')
        return data
    elif quoteType == 'CRYPTOCURRENCY':
        data = {
            'price': q['regularMarketPrice'],
            'change': q['regularMarketChange'],
            'percentchange': q['regularMarketChangePercent'],
            'low': q['regularMarketDayLow'],
            'high': q['regularMarketDayHigh'],
            'cap': int_to_human(q['marketCap']),
            'name': q['shortName'],
            'close': q['regularMarketPreviousClose'],
            'currencySymbol': cur_to_symbol(q['currency']),
            'marketState': marketState,
            'symbol': q['symbol'],
            'exchange': q['exchange']
        }
        return data
    elif quoteType in {'ECNQUOTE', 'MUTUALFUND', 'NONE'}:
        raise Exception(
            f'No data or unsupported: {bold(symbol["symbols"])} | Type: {quoteType}.')

    # marketState REGULAR and PREPRE appear to be the same thing
    # set default/catch-all data
    data = {
        'price': q['regularMarketPrice'],
        'change': q['regularMarketChange'],
        'percentchange': q['regularMarketChangePercent'],
        'low': q['regularMarketDayLow'],
        'high': q['regularMarketDayHigh'],
        'cap': int_to_human(q['marketCap']),
        'name': q['longName'],
        'close': q['regularMarketPreviousClose'],
        'currencySymbol': cur_to_symbol(q['currency']),
        'marketState': marketState,
        'symbol': q['symbol'],
        'exchange': q['exchange']
    }
    return data


def get_quote_multi(bot, symbols):
    try:
        r = requests.get(url=URL, params=symbols, headers=YHEAD)
    except requests.exceptions.ConnectionError:
        raise Exception('Unable to reach Yahoo Finance.')

    if r.status_code != 200:
        raise Exception(f'HTTP Error {r.status_code}')

    r = r.json()['quoteResponse']

    if not r["result"]:
        raise Exception('No data found. Input data likely bad.')

    r = r['result']

    # might not need this?
    data = {}
    data.clear()

    # TODO: import more data, better:
    # for Quote in Results
    for q in r:
        data[q['symbol']] = {
            'price': q['regularMarketPrice'],
            'percentchange': q['regularMarketChangePercent'],
            'currencySymbol': cur_to_symbol(q['currency'])
        }
    return data


def int_to_human(n):
    # If a stock hits a quadrillion dollar value...jesus.
    if n >= 1e15:
        return 'Holy shit!'
    # Trillions
    elif n >= 1e12:
        n = str(round(n / 1e12, 2))
        return n + 'T'
    # Billions
    elif n >= 1e9:
        n = str(round(n / 1e9, 2))
        return n + 'B'
    # Millions
    elif n >= 1e6:
        n = str(round(n / 1e6, 2))
        return n + 'M'
    # Shouldn't be anything lower than millions, but...
    return str(n)


def cur_to_symbol(currencySymbol):
    # not exhaustive; covers the top 21 exchanges https://w.wiki/4w3j
    currencies = {
        # Dollars
        'AUD': 'AU$',
        'BRL': 'R$',
        'CAD': 'C$',
        'HKD': 'HK$',
        'TWD': 'NT$',
        'USD': '$',
        # Yen/Yuan
        'CNY': 'CN¥',
        'JPY': 'JP¥',
        # Europe
        'CHF': 'CHF ',
        'EUR': '€',
        'GBP': '£',  # yes, YF really supplies both GBP and GBp...
        'GBp': '£',  # yes, YF really supplies both GBP and GBp...
        'RUB': '₽',
        # South/East Asia
        'INR': '₹',
        'IRR': 'IRR ',  # Iranian rial, not messing with RTL text...
        'KRW': '₩',
        'SAR': 'SAR ',  # Saudi riyal, not messing with RTL text...
        # Africa
        'ZAR': 'R '
    }
    # identify currencies that need to be added
    if currencySymbol not in currencies:
        cs = '?$'
    else:
        cs = currencies[currencySymbol]
    return cs


# shout-out to MrTap for this one
def name_scrubber(name):
    p = re.compile(r',? (ltd|ltee|llc|corp(oration)?|inc(orporated)?|limited|plc)\.?$', re.I)
    return p.sub('', name)


@plugin.command('oil')
@plugin.output_prefix('[OIL] ')
@plugin.rate(server=1)
def yf_oil(bot, trigger):
    """Get the latest Brent Crude Oil price per barrel."""
    # hardcode "Brent Crude Oil Last Day Financ"
    symbol = {'symbols': 'BZ=F'}

    try:
        data = get_quote(bot, symbol)
    except Exception as e:
        return bot.say(str(e))

    pchange = data['percentchange']
    if pchange >= 0:
        pchange = color(f'{pchange:+,.2f}%', colors.GREEN)
    else:
        pchange = color(f'{pchange:+,.2f}%', colors.RED)
    price = f'{data["price"]:.2f}'
    bot.say(f'PPB: ${bold(price)} ({pchange})')


@plugin.command('stock')
@plugin.rate(server=1)
def yf_stock(bot, trigger):
    """Get stock(s) info."""
    if not trigger.group(2):
        return bot.reply('I need a (list of) stock ticker(s).')

    symbols = trigger.group(3).upper()

    if re.search(',', symbols):
        symbols = {'symbols': symbols}
        try:
            data = get_quote_multi(bot, symbols)
        except Exception as e:
            return bot.say(str(e))
    else:
        symbol = {'symbols': symbols}
        try:
            data = get_quote(bot, symbol)
        except Exception as e:
            return bot.say(str(e))

    if not data:
        return

    # if multi-stock
    if 'price' not in data:
        items = []
        for symbol, attr in data.items():
            # set attrs
            cs = attr['currencySymbol']
            pchange = attr['percentchange']
            price = attr['price']
            # determine good or bad
            if pchange >= 0:
                pchange = color(f'{pchange:+,.2f}%', colors.GREEN)
                items.append(f'{symbol}: {cs}{price:,.2f} ({pchange})')
            else:
                pchange = color(f'{pchange:+,.2f}%', colors.RED)
                items.append(f'{symbol}: {cs}{price:,.2f} ({pchange})')
        # create and post msg
        return bot.say(' | '.join(items))

    # cleanup name
    data['name'] = name_scrubber(data['name'])

    # set base msg
    msg = '{name} ({symbol}) | {currencySymbol}' + bold('{price:,.2f} ')
    msg2 = ''

    # Change is None, usually on IPOs
    if not data['change']:
        msg = msg.format(**data)
    # Otherwise, check change vs previous day
    else:
        if data['change'] >= 0:
            msg += color('{change:+,.2f} {percentchange:+,.2f}%', colors.GREEN)
        else:
            msg += color('{change:+,.2f} {percentchange:+,.2f}%', colors.RED)

        msg = msg.format(**data)

    # add info if pre- or post-market
    exchange = data['exchange']
    marketState = data['marketState']
    if marketState == 'PRE' and exchange in {'NMS', 'NYQ'}:
        msg += color(' PREMARKET', colors.LIGHT_GREY)
        msg2 += ' | CLOSE {currencySymbol}{close:,.2f} '
    elif marketState in {'POST', 'POSTPOST'} and exchange in {'NMS', 'NYQ'}:
        msg += color(' POSTMARKET', colors.LIGHT_GREY)
        msg2 += ' | CLOSE {currencySymbol}{close:,.2f} '
        if data['rmchange'] >= 0:
            msg2 += color('{rmchange:+,.2f} {rmpercentchange:+,.2f}%', colors.GREEN)
        else:
            msg2 += color('{rmchange:+,.2f} {rmpercentchange:+,.2f}%', colors.RED)

    # add some more shit to the message
    msg2 += ' | '
    msg2 += color('L {low:,.2f}', colors.RED) + ' '
    msg2 += color('H {high:,.2f}', colors.GREEN)
    msg2 += ' | Cap {currencySymbol}{cap}'

    # set final message
    msg = ('{msg}' + msg2).format(msg=msg, **data)

    # finally, the bot says something!
    return bot.say(msg)
