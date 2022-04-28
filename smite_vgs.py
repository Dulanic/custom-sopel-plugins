"""
Original authors: xnaas & half_duplex (aka: mal)
License: The Unlicense (public domain)
"""
from sopel import plugin
from sopel.formatting import color, colors
import secrets


V_CMDS = {
    # VA - Attack
    "VAA": "Attack!",
    "VAF": "Attack Fire Giant!",
    "VAG": "Attack the Gold Fury!",
    "VAM": "Attack the Titan!",
    "VAN": "Attack the Minions!",
    "VA1": "Attack left lane!",
    "VA2": "Attack middle lane!",
    "VA3": "Attack right lane!",
    "VAT1": ("Attack {}!", ("left tower", "the left phoenix")),
    "VAT2": ("Attack {}!", ("middle tower", "the middle phoenix")),
    "VAT3": ("Attack {}!", ("right tower", "the right phoenix")),
    # VB - Enemy
    "VBA": "Enemy ultimate incoming!",
    "VBB": "Enemies have returned to base.",
    "VBD": "Enemy ultimate down!",
    "VBE": "Enemies behind us!",
    "VBF": "Enemies at the Fire Giant!",
    "VBG": "Enemies at the Gold Fury!",
    "VBJJ": "Enemies in the jungle!",
    "VBJ1": "Enemies in the left jungle!",
    "VBJ3": "Enemies in the right jungle!",
    "VBM": "Enemies at our Titan!",
    "VBS": "Enemy spotted!",
    "VB1": "Enemies in left lane!",
    "VB2": "Enemies in middle lane!",
    "VB3": "Enemies in right lane!",
    # VC - Careful
    "VCB": "Return to base!",
    "VCC": "Be careful!",
    "VCJ": "Be careful in the jungle!",
    "VC1": "Be careful left!",
    "VC2": "Be careful middle!",
    "VC3": "Be careful right!",
    # VD - Defend
    "VDD": "Defend!",
    "VDF": "Defend the Fire Giant!",
    "VDG": "Defend the Gold Fury!",
    "VD1": "Defend left lane!",
    "VD2": "Defend middle lane!",
    "VD3": "Defend right lane!",
    "VDM": ("Defend the {}!", ("Titan", "Portal")),
    # VE - Emote
    "VEA": "Awesome!",
    "VEG": "I'm the greatest!",
    # VEJ God jokes
    # VEL God laughs
    "VER": "You rock!",
    # VET God taunts
    "VEW": "Woohoo!",
    # VF - MIA
    "VFF": "Enemy missing!",
    "VF1": "Enemy missing left!",
    "VF2": "Enemy missing middle!",
    "VF3": "Enemy missing right!",
    # VG - Gank
    "VGG": "Gank!",
    "VG1": "Gank left lane!",
    "VG2": "Gank middle lane!",
    "VG3": "Gank right lane!",
    # VH - Help
    "VHH": "Help!",
    "VHS": "Need healing!",
    "VH1": "Help left lane!",
    "VH2": "Help middle lane!",
    "VH3": "Help right lane!",
    # VI - Incoming
    "VII": "Enemies incoming!",
    "VI1": "Enemies incoming left!",
    "VI2": "Enemies incoming middle!",
    "VI3": "Enemies incoming right!",
    # VQ - Ward
    "VQF": "Ward Fire Giant!",
    "VQG": "Ward Gold Fury!",
    "VQN": "Need Wards!",
    "VQQ": "Ward Here!",
    "VQ1": "Ward Left!",
    "VQ2": "Ward middle!",
    "VQ3": "Ward Right!",
    # VR - Retreat
    "VRJ": "Retreat from the Jungle!",
    "VRR": "Retreat!",
    "VRS": "Save yourself!",
    "VR1": "Retreat left lane!",
    "VR2": "Retreat middle lane!",
    "VR3": "Retreat right late!",
    # VS - Self
    "VSO": "I'm on it!",
    "VSR": "Falling back!",
    "VSS": "I'm building Stacks!",
    # VSA - Self Attack
    "VSAA": "I'll attack!",
    "VSAF": "I'll attack Fire Giant!",
    "VSAG": "I'll attack the Gold Fury!",
    "VSAM": "I'll attack the Titan!",
    "VSA1": "I'll attack left lane!",
    "VSA2": "I'll attack middle lane!",
    "VSA3": "I'll attack right lane!",
    # VSB - Self Buff
    "VSBB": "I'm going for jungle buff!",
    "VSBN": "I need the jungle buff!",
    "VSBT": "Take this jungle buff!",
    # VSD - Self Defend
    "VSDD": "I'll defend!",
    "VSDF": "I'll defend the Fire Giant!",
    "VSDG": "I'll defend the Gold Fury!",
    "VSDM": "I'll defend the Titan!",
    "VSD1": "I'll defend left lane!",
    "VSD2": "I'll defend middle lane!",
    "VSD3": "I'll defend right lane!",
    # VSG - Self Gank
    "VSGG": "I'll gank!",
    "VSG1": "I'll gank left lane!",
    "VSG2": "I'll gank middle lane!",
    "VSG3": "I'll gank right lane!",
    # VSQ - Self Ward
    "VSQQ": "I will ward!",
    "VSQ1": "I will ward left!",
    "VSQ2": "I will ward middle!",
    "VSQ3": "I will ward right!",
    # VST - Self Returned
    "VSTB": "I'm returning to base!",
    "VSTT": "I have returned!",
    "VST1": "I'm returning left lane!",
    "VST2": "I'm returning middle lane!",
    "VST3": "I'm returning right lane!",
    # VT - Enemies Returned
    "VTT": "Enemies have returned!",
    "VT1": "Enemies have returned left!",
    "VT2": "Enemies have returned middle!",
    "VT3": "Enemies have returned right!",
    # VV - Other
    "VVA": "Ok!",
    "VVB": "Be right back!",
    "VVC": "Completed!",
    "VVK": "Stepping away for a moment.",
    "VVM": "Out of mana!",
    "VVN": "No!",
    "VVP": "Please?",
    "VVS": "Sorry!",
    "VVT": "Thanks!",
    "VVW": "Wait!",
    "VVX": "Cancel that!",
    "VVY": "Yes!",
    # VVG - General
    "VVGB": "Bye!",
    "VVGF": "Have fun!",
    "VVGG": "Good game!",
    "VVGH": "Hi!",
    "VVGL": "Good luck!",
    "VVGN": "Nice job!",
    "VVGO": "Oops!",
    "VVGQ": "Quiet!",
    "VVGR": "No problem!",
    "VVGS": "Curses!",
    "VVGT": "That's too bad!",
    "VVGW": "You're welcome!",
    # VVV - Position
    "VVVA": "Set up an ambush here!",
    "VVVB": "Behind us!",
    "VVVC": "Chase the enemy!",
    # VVVD Ultimate is down! - special case
    "VVVE": "On my way!",
    "VVVF": "Follow me!",
    "VVVG": "Group up!",
    "VVVJ": "Going into the jungle!",
    "VVVP": "Split push!",
    "VVVR": "Ultimate is ready!",
    "VVVS": "Stay here!",
    "VVVT": "It's a trap!",
    "VVVW": "Place a Ward for teleport!",
    "VVVX": "Spread Out!",
    # VX - Social Emotes
    # VXW [Wave]
    # VXD [Dance]
    # VXC [Clap]
    # VXS [Special]
    # VXF [Furious]
    # VXG [Special 2]
    # VXE [Global Emote]
}


@plugin.rule(r"^V[ABCDEFGHIQRSTVX][A-Z1-9]{1,2}$")
def vgs_va_easy(bot, trigger):
    cmd = trigger.group(0).upper()
    nick_fmt = color("\u200B".join(trigger.nick), colors.CYAN)
    if cmd in V_CMDS:
        msg = V_CMDS[cmd]
        if isinstance(msg, tuple):
            msg = msg[0].format(secrets.choice(msg[1]))
        bot.say(nick_fmt + color(f": [{cmd}] {msg}", colors.SILVER))
    elif cmd == "VVVD":
        time = secrets.randbelow(1401) / 10
        bot.say(
            nick_fmt +
            color(
                f": [{cmd}] Ultimate is down! ({time:0.2f} remaining)",
                colors.SILVER))
    else:
        return plugin.NOLIMIT
