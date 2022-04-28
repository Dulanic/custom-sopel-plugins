"""
Original author: xnaas
License: The Unlicense (public domain)
"""
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
def osrs_base(bot, trigger):
    cmd = trigger.group(1).lower()

    if cmd == "osrs":
        if trigger.is_privmsg:
            return bot.reply("This command must be used in a channel.")
        target = plain(trigger.group(3) or trigger.nick)
        target = tools.Identifier(target)
        if target == bot.nick:
            return bot.reply("I don't play OSRS, because I have a life.")
        if target not in bot.channels[trigger.sender].users:
            return bot.reply("Please provide a valid user.")
        osrs(bot, trigger, target)

    elif cmd == "osrs set":
        osrs_set(bot, trigger)

    elif cmd == "osrs settype":
        osrs_settype(bot, trigger)

    elif cmd == "osrs stats":
        target = plain(trigger.group(2))
        if not target:
            return bot.reply("Please provide an OSRS character name.")
        osrs(bot, trigger, target, general_check=True)

    elif cmd == "osrs pcount":
        osrs_pcount(bot, trigger)

    elif cmd == "osrs wiki":
        # msg = osrs_wiki()
        return bot.say("Wiki commands not implemented yet.")

    elif cmd == "osrs help":
        osrs_help(bot, trigger)


def osrs_set(bot, trigger):
    user = trigger.nick
    osrs_name = plain(trigger.group(2) or '')
    if not osrs_name:
        return bot.reply("Please provide your OSRS character name.")
    bot.db.set_nick_value(user, "osrs_name", osrs_name)
    return bot.say(f"Successfully set your OSRS name as {bold(osrs_name)}.")


def osrs_settype(bot, trigger):
    user = trigger.nick
    type = plain(trigger.group(2).lower() or '')
    if type in VALID_TYPES:
        bot.db.set_nick_value(user, "osrs_type", type)
        return bot.reply(f"You've configured your character to use the {type} hiscores.")
    else:
        return bot.reply(f"Please provide a valid type: {', '.join(VALID_TYPES)}")


def osrs(bot, trigger, target, general_check=False):
    if general_check == False:
        name = bot.db.get_nick_value(target, "osrs_name")
        type = bot.db.get_nick_value(target, "osrs_type")
        if not name:
            return bot.say(f"{target} has no OSRS name set. They must use `.osrs set <name>`")
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
        return bot.say(f"Invalid type set for {bold(target)}.")

    param = {"player": name}
    try:
        data = requests.get(url, params=param)
    except requests.exceptions.ConnectionError:
        return bot.say("Error reaching API.")

    if data.status_code != 200:
        msg = f"HTTP Error {data.status_code}"
        if data.status_code == 404:
            return bot.say(f"{bold(name)} not found.")

    data = data.text.split(maxsplit=24)[:-1]  # cut off non-skill data
    skills = {}
    i = 0
    for skill in data:
        skill = skill.split(",")
        skills.update({SKILL_LIST[i]: skill[1]})
        i += 1

    # check for max
    if skills["Overall"] == "2277":
        return bot.say(f"{bold(name)} has their Max Cape! 🎊")

    # get combat lvl, set total xp
    cmbt_lvl = osrs_cmbt_lvl(skills)
    total_xp = int(data[0].split(",")[2])
    skills.update({"XP": f"{total_xp:,}"})

    # layout msg
    msg = f"{name} (⚔{cmbt_lvl}):"
    msg += " Total {Overall} | XP {XP}"
    msg += " | Atk {Attack} | Str {Strength} | Def {Defence} | Range {Ranged}"
    msg += " | Pray {Prayer} | Mage {Magic} | RC {Runecrafting} | Con {Construction}"
    msg += " | HP {Hitpoints} | Agi {Agility} | Herb {Herblore} | Thief {Thieving}"
    msg += " | Craft {Crafting} | Fletch {Fletching} | Slayer {Slayer} | Hunt {Hunter}"
    msg += " | Mine {Mining} | Smith {Smithing} | Fish {Fishing} | Cook {Cooking}"
    msg += " | FM {Firemaking} | WC {Woodcutting} | Farm {Farming}"
    msg = msg.format(**skills)
    return bot.say(msg)


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


def osrs_pcount(bot, trigger):
    url = "https://oldschool.runescape.com"
    try:
        raw = requests.get(url)
    except requests.exceptions.ConnectionError:
        return bot.say("Error reaching API.")
    html = BeautifulSoup(raw.text, "html.parser")
    msg = html.select_one(".player-count").string
    return bot.say(msg)


def osrs_help(bot, trigger):
    # inform about DM spam
    dm_warn = "I am DM'ing you all OSRS help, as it's quite long."
    bot.say(dm_warn)
    # DM spam
    msg = "`.osrs` or `.osrs <nick>` is used to lookup your or another IRC user's OSRS character.\n"
    msg += "`.osrs set <name>` is used to set your OSRS character name for use with `.osrs`.\n"
    msg += "`.osrs settype <type>` is used to set which hiscores table to lookup your character on."
    msg += f" Valid types are: {', '.join(VALID_TYPES)}."
    msg += " If no type is specified, then the regular hiscores table will be used.\n"
    msg += "`.osrs stats <name>` is used to lookup the stats of any OSRS character name.\n"
    msg += "`.osrs pcount` will list the current number of OSRS players in-game.\n"
    msg += "`.osrs wiki <search terms>` is not yet implemented. Sorry!"
    for line in msg.splitlines():
        bot.notice(line, trigger.nick)
