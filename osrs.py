from math import floor as round_down
from sopel import plugin, tools
from sopel.formatting import bold, plain
import re
import requests


BASE_URL = "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws"


@plugin.commands("osrs set", "osrs stats", "osrs wiki", "osrs help", "osrs")
@plugin.output_prefix("[OSRS] ")
@plugin.require_chanmsg
def osrs_base(bot, trigger):
    cmd = trigger.group(1)

    if re.fullmatch("osrs", cmd, re.IGNORECASE):
        target = plain(trigger.group(3) or trigger.nick)
        target = tools.Identifier(target)
        if target == bot.nick:
            return bot.reply("I don't play OSRS, because I have a life.")
        # TODO: (below) is there a more "global" check...?
        #       requiring @plugin.require_chanmsg kinda
        #       sucks, so... 🙃
        if target not in bot.channels[trigger.sender].users:
            return bot.reply("Please provide a valid user.")
        msg = osrs(bot, trigger, target)
    elif re.fullmatch("osrs set", cmd, re.IGNORECASE):
        user = trigger.nick
        osrs_name = plain(trigger.group(2) or '')
        if not osrs_name:
            return bot.reply("Please provide your OSRS character name.")
        msg = osrs_set(bot, trigger, user, osrs_name)
    elif re.fullmatch("osrs stats", cmd, re.IGNORECASE):
        target = plain(trigger.group(2))
        if not target:
            return bot.reply("Please provide an OSRS character name.")
        msg = osrs(bot, trigger, target, general_check=True)
    elif re.fullmatch("osrs wiki", cmd, re.IGNORECASE):
        # msg = osrs_wiki()
        return bot.say("Wiki commands not implemented yet.")
    elif re.fullmatch("osrs help", cmd, re.IGNORECASE):
        msg = "I am DM'ing you all OSRS help, as it's quite long."
        bot.say(msg)
        msg1 = "`.osrs` or `.osrs <nick>` is used to lookup your or another IRC user's OSRS character. "
        msg2 = "`.osrs set <name>` is used to set your OSRS character name for use with `.osrs`. "
        msg3 = "`.osrs stats <name>` is used to lookup the stats of any OSRS character name. "
        msg4 = "`.osrs wiki <search terms>` is not yet implemented. Sorry!"
        msgs = [msg1, msg2, msg3, msg4]
        for msg_id in msgs:
            bot.notice(msg_id, trigger.nick)
        return

    return bot.say("{}".format(msg))


def osrs_set(bot, trigger, user, osrs_name):
    bot.db.set_nick_value(user, "osrs_name", osrs_name)
    msg = "Successfully set your OSRS name as {}.".format(bold(osrs_name))
    return msg


def osrs(bot, trigger, target, general_check=False):
    if general_check == False:
        name = bot.db.get_nick_value(target, "osrs_name")
        if not name:
            msg = "{} has no OSRS name set. They must use `.osrs set <name>`".format(target)
            return msg
    elif general_check == True:
        name = target

    param = {"player": name}
    try:
        data = requests.get(BASE_URL, params=param)
    except requests.exceptions.ConnectionError:
        msg = "Error reaching API."
        return msg

    if data.status_code != 200:
        msg = "HTTP Error {}".format(data.status_code)
        if data.status_code == 404:
            msg = "{} not found.".format(bold(name))
        return msg

    data = data.text.rsplit(maxsplit=60)[0]  # cut off all non-skill data
    data = data.split()  # split each skill
    skills = []  # blank list
    for skill in data:
        skill = skill.split(",")
        skills.append(skill[1])

    # check for max
    if skills[0] == "2277":
        msg = "{name} has their Max Cape! 🎊".format(name=bold(name))
        return msg

    # get combat lvl
    cmbt_lvl = osrs_cmbt_lvl(skills)

    # layout msg
    msg = "{name} (⚔{cmbt_lvl}): Total {s[0]}"
    msg += " | Atk {s[1]} | Def {s[2]} | Str {s[3]} | HP {s[4]}"
    msg += " | Range {s[5]} | Pray {s[6]} | Mage {s[7]} | Cook {s[8]}"
    msg += " | WC {s[9]} | Fletch {s[10]} | Fish {s[11]} | FM {s[12]}"
    msg += " | Craft {s[13]} | Smith {s[14]} | Mine {s[15]} | Herb {s[16]}"
    msg += " | Agi {s[17]} | Thief {s[18]} | Slayer {s[19]} | Farm {s[20]}"
    msg += " | RC {s[21]} | Hunt {s[22]} | Con {s[23]}"

    # TODO: perhaps craft a dict instead of a list
    #       so we can just do format(**skills) or
    #       something like that.
    msg = msg.format(name=name, s=skills, cmbt_lvl=cmbt_lvl)
    return msg


def osrs_cmbt_lvl(skills):
    # set skills to calc combat lvl
    atk = int(skills[1])
    defence = int(skills[2])
    strength = int(skills[3])
    hp = int(skills[4])
    ranged = int(skills[5])
    prayer = int(skills[6])
    mage = int(skills[7])

    # calc base combat lvl
    base_cmbt_lvl = round_down(prayer/2)
    base_cmbt_lvl = (base_cmbt_lvl + hp + defence)/4

    # calc combat lvls
    melee_cmbt_lvl = (strength + atk) * 0.325
    range_cmbt_lvl = (round_down(ranged/2) + ranged) * 0.325
    mage_cmbt_lvl = (round_down(mage/2) + mage) * 0.325

    # finally get combat lvl
    cmbt_lvl = base_cmbt_lvl + max(melee_cmbt_lvl, range_cmbt_lvl, mage_cmbt_lvl)
    cmbt_lvl = round(cmbt_lvl, 2)

    # return combat lvl
    return cmbt_lvl
