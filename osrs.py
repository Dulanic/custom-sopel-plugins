from bs4 import BeautifulSoup
from math import floor as round_down
from sopel import plugin, tools
from sopel.formatting import bold, plain
import requests


HISCORES_ALL = "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws"
HISCORES_IM = "https://secure.runescape.com/m=hiscore_oldschool_ironman/index_lite.ws"
HISCORES_UIM = "https://secure.runescape.com/m=hiscore_oldschool_ultimate/index_lite.ws"
HISCORES_HCIM = "https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/index_lite.ws"
SKILL_LIST = [  # order from API
    "Overall", "Attack", "Defence", "Strength", "Hitpoints", "Ranged", "Prayer",
    "Magic", "Cooking", "Woodcutting", "Fletching", "Fishing", "Firemaking",
    "Crafting", "Smithing", "Mining", "Herblore", "Agility", "Thieving", "Slayer",
    "Farming", "Runecrafting", "Hunter", "Construction"]
VALID_TYPES = ["im", "hcim", "uim"]


@plugin.commands("osrs settype", "osrs set", "osrs stats",
                "osrs pcount", "osrs wiki", "osrs help", "osrs")
@plugin.output_prefix("[OSRS] ")
@plugin.require_chanmsg
def osrs_base(bot, trigger):
    cmd = trigger.group(1).lower()

    if cmd == "osrs":
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

    elif cmd == "osrs set":
        user = trigger.nick
        osrs_name = plain(trigger.group(2) or '')
        if not osrs_name:
            return bot.reply("Please provide your OSRS character name.")
        msg = osrs_set(bot, trigger, user, osrs_name)

    elif cmd == "osrs settype":
        user = trigger.nick
        type = plain(trigger.group(2).lower() or '')
        msg = osrs_settype(bot, trigger, user, type)

    elif cmd == "osrs stats":
        target = plain(trigger.group(2))
        if not target:
            return bot.reply("Please provide an OSRS character name.")
        msg = osrs(bot, trigger, target, general_check=True)

    elif cmd == "osrs pcount":
        msg = osrs_pcount()

    elif cmd == "osrs wiki":
        # msg = osrs_wiki()
        return bot.say("Wiki commands not implemented yet.")

    elif cmd == "osrs help":
        osrs_help(bot, trigger)
        return

    return bot.say(msg)


def osrs_set(bot, trigger, user, osrs_name):
    bot.db.set_nick_value(user, "osrs_name", osrs_name)
    msg = "Successfully set your OSRS name as {}.".format(bold(osrs_name))
    return msg


def osrs_settype(bot, trigger, user, type):
    if type in VALID_TYPES:
        bot.db.set_nick_value(user, "osrs_type", type)
        msg = "You've configured your character to use the {} hiscores, {}.".format(type, user)
    else:
        msg = "Please provide a valid type: {}".format(", ".join(VALID_TYPES))
    return msg


def osrs(bot, trigger, target, general_check=False):
    if general_check == False:
        name = bot.db.get_nick_value(target, "osrs_name")
        type = bot.db.get_nick_value(target, "osrs_type")
        if not name:
            msg = "{} has no OSRS name set. They must use `.osrs set <name>`".format(target)
            return msg
    elif general_check == True:
        name = target
        type = None

    # configure which URL to use
    if not type:
        url = HISCORES_ALL
    elif type == "im":
        url = HISCORES_IM
    elif type == "hcim":
        url = HISCORES_HCIM
    elif type == "uim":
        url = HISCORES_UIM
    else:
        msg = "Invalid type set for {}.".format(bold(target))
        return msg

    param = {"player": name}
    try:
        data = requests.get(url, params=param)
    except requests.exceptions.ConnectionError:
        msg = "Error reaching API."
        return msg

    if data.status_code != 200:
        msg = "HTTP Error {}".format(data.status_code)
        if data.status_code == 404:
            msg = "{} not found.".format(bold(name))
        return msg

    data = data.text.rsplit(maxsplit=61)[0]  # cut off all non-skill data
    data = data.split()  # split each skill
    skills = {}  # init empty dict
    i = 0
    for skill in data:
        skill = skill.split(",")
        skills.update({SKILL_LIST[i]: skill[1]})
        i += 1

    # check for max
    if skills["Overall"] == "2277":
        msg = "{name} has their Max Cape! 🎊".format(name=bold(name))
        return msg

    # get combat lvl, set total xp
    cmbt_lvl = osrs_cmbt_lvl(skills)
    skills.update({"XP": "{:,}".format(int(data[0].split(",")[2]))})

    # layout msg
    msg = "{name} (⚔{cmbt_lvl}):".format(name=name, cmbt_lvl=cmbt_lvl)
    msg += " Total {Overall} | XP {XP}"
    msg += " | Atk {Attack} | Str {Strength} | Def {Defence} | Range {Ranged}"
    msg += " | Pray {Prayer} | Mage {Magic} | RC {Runecrafting} | Con {Construction}"
    msg += " | HP {Hitpoints} | Agi {Agility} | Herb {Herblore} | Thief {Thieving}"
    msg += " | Craft {Crafting} | Fletch {Fletching} | Slayer {Slayer} | Hunt {Hunter}"
    msg += " | Mine {Mining} | Smith {Smithing} | Fish {Fishing} | Cook {Cooking}"
    msg += " | FM {Firemaking} | WC {Woodcutting} | Farm {Farming}"
    msg = msg.format(**skills)
    return msg


def osrs_cmbt_lvl(skills):
    # set skills to calc combat lvl
    atk = int(skills["Attack"])
    defence = int(skills["Defence"])
    strength = int(skills["Strength"])
    hp = int(skills["Hitpoints"])
    ranged = int(skills["Ranged"])
    prayer = int(skills["Prayer"])
    mage = int(skills["Magic"])

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


def osrs_pcount():
    url = "https://oldschool.runescape.com"
    try:
        raw = requests.get(url)
    except requests.exceptions.ConnectionError:
        msg = "Error reaching API."
        return msg

    html = BeautifulSoup(raw.text, "html.parser")
    msg = html.select_one(".player-count").string

    return msg


def osrs_help(bot, trigger):
    # inform about DM spam
    dm_warn = "I am DM'ing you all OSRS help, as it's quite long."
    bot.say(dm_warn)
    # DM spam
    msg = "`.osrs` or `.osrs <nick>` is used to lookup your or another IRC user's OSRS character.\n"
    msg += "`.osrs set <name>` is used to set your OSRS character name for use with `.osrs`.\n"
    msg += "`.osrs settype <type>` is used to set which hiscores table to lookup your character on."
    msg += " Valid types are: {}.".format(", ".join(VALID_TYPES))
    msg += " If no type is specified, then the regular hiscores table will be used.\n"
    msg += "`.osrs stats <name>` is used to lookup the stats of any OSRS character name.\n"
    msg += "`.osrs pcount` will list the current number of OSRS players in-game.\n"
    msg += "`.osrs wiki <search terms>` is not yet implemented. Sorry!"
    for line in msg.splitlines():
        bot.notice(line, trigger.nick)
    return
