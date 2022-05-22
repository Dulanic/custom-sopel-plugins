"""
Authors: xnaas (2022)
License: The Unlicense (public domain)
"""
import requests
from sopel import plugin
from sopel.formatting import color, colors, plain


AB_URL = 'https://status.animebytes.tv/api/status'
TS_URL = 'https://{}.trackerstatus.info/api/all'


@plugin.command('ab', 'btn', 'ggn', 'ptp', 'red')
@plugin.rate(server=1)
@plugin.require_chanmsg
def one_hundred_percent_legal_service_status(bot, trigger):
    # get command and sub-command, if present
    cmd = trigger.group(1).lower()
    subcmd = plain(trigger.group(2) or '').lower()

    if cmd == 'ab':
        try:
            msg = ab_status()
        except Exception as e:
            bot.say(str(e))
            return plugin.NOLIMIT
    else:
        try:
            msg = trackerstatus(subcmd, cmd)
        except Exception as e:
            bot.say(str(e))
            return plugin.NOLIMIT

    bot.say(f'[{cmd.upper()}] {msg}')


def ab_status():
    try:
        r = requests.get(AB_URL).json()['status']
    except Exception:
        raise Exception('Error reaching API, probably.')

    # create a list of each service's status
    statuses = [service['status'] for service in r.values()]

    # convert status int to colored text
    for index, status in enumerate(statuses):
        if status == 1:
            statuses[index] = color('Online', colors.GREEN)
        elif status == 0:
            statuses[index] = color('Offline', colors.RED)
        # tracker can have a partial outage
        elif status == 2 and index == 0:
            statuses[index] = color('Partial Outage', colors.YELLOW)
        # site can be in maintenance mode
        elif status == 2 and index == 1:
            statuses[index] = color('Maintenance', colors.YELLOW)
        else:
            statuses[index] = color('???', colors.ORANGE)

    # format msg, assumes order from API is always the same
    msg =  f'Site: {statuses[1]} | Mei: {statuses[3]} | '
    msg += f'Tracker: {statuses[0]} | IRC: {statuses[2]}'
    return msg


def trackerstatus(subcmd, service):
    # TODO: do something with subcommands...uptime, downtime, something?
    if not subcmd:
        pass

    try:
        r = requests.get(TS_URL.format(service))
    except Exception:
        raise Exception('Error reaching API, probably.')

    # init a blank status list
    statuses = []
    # all trackers have these 3
    statuses.append(int(r.json()['Website']['Status']))
    statuses.append(int(r.json()['TrackerHTTP']['Status']))
    statuses.append(int(r.json()['TrackerHTTPS']['Status']))

    if service == 'btn':
        statuses.append(int(r.json()['IRC']['Status']))
        statuses.append(int(r.json()['CableGuy']['Status']))
        statuses.append(int(r.json()['Barney']['Status']))
    elif service == 'ptp':
        statuses.append(int(r.json()['IRCPersona']['Status']))
        statuses.append(int(r.json()['IRCUserIdentifier']['Status']))
        statuses.append(int(r.json()['IRCTorrentAnnouncer']['Status']))
    elif service == 'red':
        statuses.append(int(r.json()['IRC']['Status']))
        statuses.append(int(r.json()['IRCUserIdentifier']['Status']))
        statuses.append(int(r.json()['IRCTorrentAnnouncer']['Status']))

    for index, status in enumerate(statuses):
        if status == 1:
            statuses[index] = color('Online', colors.GREEN)
        elif status == 0:
            statuses[index] = color('Offline', colors.RED)
        elif status == 2:
            statuses[index] = color('Unstable', colors.YELLOW)
        else:
            statuses[index] = color('???', colors.ORANGE)

    msg = "Website: {} | TrackerHTTP: {} | TrackerHTTPS: {}"
    if len(statuses) == 3:
        pass
    elif len(statuses) == 6:
        msg += " | IRC: {} | IRC Ident: {} | Torrent Announcer: {}"
    else:
        raise Exception('Something went horribly wrong...')

    return msg.format(*statuses)
