"""
Original author: xnaas (2020-2022+)
License: The Unlicense (public domain)
"""
from os import listdir
from secrets import choice as choose
from sopel import plugin
from sopel.formatting import bold, italic, monospace, plain


DOMAIN = "https://p.actionsack.com/"
PATH = "/mnt/media/websites/p.actionsack.com/"


@plugin.search("!nod")
@plugin.command("nod")
def nod(bot, trigger):
    """Nod.
    Can also be triggered with '!nod' anywhere in a message."""
    bot.say(f"{DOMAIN}trek/nod.webp")


@plugin.search("!spok")
@plugin.command("spok")
def spok(bot, trigger):
    """Summon SPOK into chat.
    Can also be triggered with '!spok' anywhere in a message."""
    bot.say(f"{DOMAIN}trek/spok.webp")


@plugin.search("!cube")
@plugin.command("cube")
def trek_cube(bot, trigger):
    """Can also be triggered with '!cube' anywhere in a message."""
    bot.say(f"{DOMAIN}trek/cube.webp")


@plugin.rule(r"^Hello(\?|!)$")
def hi(bot, trigger):
    bot.say(f"Hello, {trigger.nick}!")


@plugin.rule(r"^(Nice\.)(\s$|$)")
def nice(bot, trigger):
    bot.say(trigger.group(1))


@plugin.rule(r"^(This\sis\sThe\sWay\.)($|\s$)")
def theway(bot, trigger):
    bot.say(trigger.group(1))


@plugin.rule(r"^(It\sis\sknown\.)(\s$|$)")
def itisknown(bot, trigger):
    bot.say(trigger.group(1))


@plugin.rule("^yeah!$")
def yeah(bot, trigger):
    bot.say(f"{DOMAIN}misc/yeah!.webp")


@plugin.rule("^retard.*")
def retarded(bot, trigger):
    bot.say(f"{DOMAIN}retard/{choose(listdir(f'{PATH}retard'))}")


@plugin.search("rekt")
def rekt(bot, trigger):
    rekt = [
        f"{DOMAIN}rekt/baseball.gif",
        f"{DOMAIN}rekt/beachdive.mp4",
        f"{DOMAIN}rekt/beachskillz.gif",
        f"{DOMAIN}rekt/bf1revenge.mp4",
        f"{DOMAIN}rekt/bf1sniper.mp4",
        f"{DOMAIN}rekt/blackman.gif",
        f"{DOMAIN}rekt/botw-sled.gif",
        f"{DOMAIN}rekt/calligraphy.mp4",
        f"{DOMAIN}rekt/carcrash.gif",
        f"{DOMAIN}rekt/dive.gif",
        f"{DOMAIN}rekt/ForHonor.webm",
        f"{DOMAIN}rekt/gta-bike.mp4",
        f"{DOMAIN}rekt/gta-bounce.mp4",
        f"{DOMAIN}rekt/gta-cop.mp4",
        f"{DOMAIN}rekt/gta-flight.mp4",
        f"{DOMAIN}rekt/gta-gas.mp4",
        f"{DOMAIN}rekt/gta-phone.mp4",
        f"{DOMAIN}rekt/gta-post.mp4",
        f"{DOMAIN}rekt/gta-rekt.mp4",
        f"{DOMAIN}rekt/gta-stomp.gif",
        f"{DOMAIN}rekt/gta-walkitoff.mp4",
        f"{DOMAIN}rekt/jeep.gif",
        f"{DOMAIN}rekt/leap.gif",
        f"{DOMAIN}rekt/LOLOLOLOL.gif",
        f"{DOMAIN}rekt/poolgirl.gif",
        f"{DOMAIN}rekt/pubg-redzone.mp4",
        f"{DOMAIN}rekt/rekt.png",
        f"{DOMAIN}rekt/running.gif",
        f"{DOMAIN}rekt/shionXclayman.webp",
        f"{DOMAIN}rekt/skateit.mp4",
        f"{DOMAIN}rekt/slammin.gif",
        f"{DOMAIN}rekt/smash.mp4",
        f"{DOMAIN}rekt/sniped.mp4",
        f"{DOMAIN}rekt/walkbot.gif",
        f"{DOMAIN}rekt/watergun.gif",
        "https://w.wiki/n9f"
    ]
    bot.say(choose(rekt))


@plugin.rule("^420.*")
def fourtwenty(bot, trigger):
    bot.say(f"{DOMAIN}420/{choose(listdir(f'{PATH}420'))}")


@plugin.search(":retardeyes:")
def retardeyes(bot, trigger):
    bot.say(f"{DOMAIN}emoji/retardeyes.webp")


@plugin.search(":wesmart:")
def wesmart(bot, trigger):
    wesmarts = [
        f"{DOMAIN}emoji/wesmart.webp",
        f"{DOMAIN}pepe/wesmart.webp"
    ]
    bot.say(choose(wesmarts))


@plugin.rule("^thx.*")
def thx(bot, trigger):
    bot.say(f"{DOMAIN}thx/thx.png")


@plugin.rule(r"^(thanks|thank\syou).*")
def thanks(bot, trigger):
    bot.say(f"{DOMAIN}thx/{choose(listdir(f'{PATH}thx'))}")


@plugin.rule("^😢$")
@plugin.command("cry")
def crying(bot, trigger):
    """Bot will reply with a crying GIF or emoticon.
    Can also be summoned by sending a message that is only the 😢 emoji."""
    crying = [
        f"{DOMAIN}QQ/QQ000.webp",
        f"{DOMAIN}QQ/QQ001.webp",
        f"{DOMAIN}QQ/QQ002.webp",
        f"{DOMAIN}QQ/QQ003.webp",
        f"{DOMAIN}QQ/QQ004.webp",
        f"{DOMAIN}QQ/QQ005.webp",
        f"{DOMAIN}QQ/QQ006.webp",
        f"{DOMAIN}QQ/QQ007.webp",
        "ಥ_ಥ",
        "＞︿＜",
        "＞﹏＜",
        "X﹏X",
        "T_T"
    ]
    bot.say(choose(crying))


@plugin.search("!pat(?!ch)")
@plugin.command("pat")
def pat(bot, trigger):
    bot.say(f"{DOMAIN}pat/{choose(listdir(f'{PATH}pat'))}")


@plugin.search("cry me a river")
def cryriver(bot, trigger):
    bot.say(f"{DOMAIN}QQ/QQ007.webp")


@plugin.search("!bge")
@plugin.commands("bge")
def bge(bot, trigger):
    """Can also be triggered with '!bge' anywhere in a message."""
    bot.say("https://ott.actionsack.com/room/ASAK")


@plugin.search("📖")
def book(bot, trigger):
    bot.say(f"{DOMAIN}mike/📖/{choose(listdir(f'{PATH}mike/📖'))}")


@plugin.rule("^8D$")
def greg(bot, trigger):
    bot.say("Greg was never in IRC...")


@plugin.rule(r"\bgrimm\b")
def grim(bot, trigger):
    bot.say("Probably still showering with his sister to this day...")


@plugin.rule("^FOAD.*")
def foad(bot, trigger):
    bot.say(f"{DOMAIN}misc/foad.png")


@plugin.search("adapters")
def adapters(bot, trigger):
    bot.say(f"{DOMAIN}adapters/{choose(listdir(f'{PATH}adapters'))}")


@plugin.search(r"accident\b")
def accident(bot, trigger):
    bot.say(f"{DOMAIN}misc/accident.webp")


@plugin.search("14nm")
def fourteennm(bot, trigger):
    bot.say(f"{DOMAIN}misc/14nm+++++.mp4")


@plugin.search("bait")
def bait(bot, trigger):
    bot.say(f"{DOMAIN}bait/{choose(listdir(f'{PATH}bait'))}")


@plugin.search("backhand")
def backhand(bot, trigger):
    bot.say(f"{DOMAIN}misc/backhand.mp4")


@plugin.rule("^😠$")
def angryeyes(bot, trigger):
    bot.say(f"{DOMAIN}misc/angryeyes.webp")


@plugin.search(r"\balot\b")
def alot(bot, trigger):
    bot.say(f"{DOMAIN}alot/")


@plugin.search("♿")
def handicap(bot, trigger):
    bot.say(f"{DOMAIN}♿/♿.mp4")


@plugin.search("⤵️")
def down(bot, trigger):
    bot.say(f"{DOMAIN}mike/down.gif")


@plugin.rule(r"^\.\.\.$")
def dotdotdot(bot, trigger):
    bot.say("...")


@plugin.search("deez nut(s|z)")
@plugin.command("dz")
def deeznutz(bot, trigger):
    """Can also be triggered with "deez nutz" or "deez nuts" anywhere in a message."""
    deez_nutz = [
        bold("DEEZ NUTZ!"),
        f"{DOMAIN}nutz/aldeez.webp",
        f"{DOMAIN}nutz/dd.webp",
        f"{DOMAIN}nutz/dragon.webp",
        f"{DOMAIN}nutz/grandma.webp",
        f"{DOMAIN}nutz/new_world.webp",
        f"{DOMAIN}nutz/prez.webp",
        f"{DOMAIN}nutz/wood.webp"
    ]
    bot.say(choose(deez_nutz))


@plugin.command("lenny", "rlenny")
def rlenny(bot, trigger):
    """Sends a random ( ͡° ͜ʖ ͡°) variation...or a GIF/MP4!"""
    rlenny = [
        f"{DOMAIN}lenny/anime.gif",
        f"{DOMAIN}lenny/crazy.mp4",
        f"{DOMAIN}lenny/spiral.gif",
        "( ͡° ͜ʖ ͡°)",
        "(☭ ͜ʖ ☭)",
        "( ° ͜ʖ °)",
        "(⟃ ͜ʖ ⟄) ",
        "( ‾ ʖ̫ ‾)",
        "( ͡° ʖ̯ ͡°)",
        "ʕ ͡° ʖ̯ ͡°ʔ",
        "( ͡° ل͜ ͡°)",
        "( ͡o ͜ʖ ͡o)",
        "( ͡◉ ͜ʖ ͡◉)",
        "( ͡☉ ͜ʖ ͡☉)",
        "ʕ ͡° ͜ʖ ͡°ʔ",
        "( ͡ᵔ ͜ʖ ͡ᵔ )",
        r"¯\_( ͡° ͜ʖ ͡°)_/¯",
        "(͡ ͡° ͜ つ ͡͡°)"
    ]
    bot.say(choose(rlenny))


@plugin.command("tableflip", "tflip")
def tableflip(bot, trigger):
    bot.say("(╯°□°）╯︵ ┻━┻")


@plugin.search(r"\(╯°□°）╯︵ ┻━┻")
def unflip(bot, trigger):
    bot.say(f"┬─┬﻿ ノ( ゜-゜ノ) — Please respect tables, {trigger.nick}.")


@plugin.rule("^pranked!$")
def prank(bot, trigger):
    bot.say(f"{DOMAIN}prank/{choose(listdir(f'{PATH}prank'))}")


@plugin.rule(r"^\?{3,}$")
def que(bot, trigger):
    bot.say(f"{DOMAIN}misc/¿¿¿.webp")


@plugin.rule(r"^\\o/$")
def handsup(bot, trigger):
    bot.say("\\o/")


@plugin.command("shrug")
@plugin.rule(r"^¯\\\_\(ツ\)_\/¯(\s$|$)")
def shrug(bot, trigger):
    bot.say("¯\\_(ツ)_/¯")


@plugin.search("🦏")
def rhino(bot, trigger):
    bot.say(f"{DOMAIN}🦏/🦏.webp")


@plugin.search("🧀")
def cheese(bot, trigger):
    bot.say(f"{DOMAIN}🧀/🧀.mp4")


@plugin.search("🦄")
def unicorn(bot, trigger):
    bot.say(f"{DOMAIN}🦄/🦄.webp")


@plugin.rule("^🙃$")
def upsidedown(bot, trigger):
    bot.say("🙃")


@plugin.rule("^🖕(|🏻|🏼|🏽|🏾|🏿)$")
def fuckyouback(bot, trigger):
    bot.say(f"Fuck you, {trigger.nick}!")


@plugin.rule("^👏$")
def clap(bot, trigger):
    bot.say("👏🏻👏🏼👏🏽👏🏾👏🏿")


@plugin.rule("^👍$")
def thumbsup(bot, trigger):
    bot.say("👍🏻👍🏼👍🏽👍🏾👍🏿")


@plugin.rule("^👎$")
def thumbsdown(bot, trigger):
    bot.say("👎🏻👎🏼👎🏽👎🏾👎🏿")


@plugin.rule("^👌$")
def okhand(bot, trigger):
    bot.say("👌🏻👌🏼👌🏽👌🏾👌🏿")


@plugin.rule("^👋$")
def wave(bot, trigger):
    bot.say("👋🏻👋🏼👋🏽👋🏾👋🏿")


@plugin.rule("^🖖$")
def vulcansalute(bot, trigger):
    bot.say("🖖🏻🖖🏼🖖🏽🖖🏾🖖🏿")


@plugin.rule("^💪$")
def muscle(bot, trigger):
    bot.say("💪🏻💪🏼💪🏽💪🏾💪🏿")


@plugin.rule("^🤞$")
def crossed(bot, trigger):
    bot.say("🤞🏻🤞🏼🤞🏽🤞🏾🤞🏿")


@plugin.search("(🌎|🌍|🌏)")
def earthchan(bot, trigger):
    bot.say(f"{DOMAIN}🌎/water.png")


@plugin.rule("^🐉$")
def dragon(bot, trigger):
    bot.say("https://p.xnaas.info/dragon.gif")


@plugin.rule("^🏈$")
def football(bot, trigger):
    football = [
        "D'Marcus Williums",
        "T.J. Juckson",
        "T'varisuness King",
        "Jackmerius Tacktheritrix",
        "D'Squarius Green, Jr.",
        "Dan Smith",
        "The Player Formerly Known as Mousecop",
        "Ibrahim Moizoos",
        "D'Isiah T. Billings-Clyde",
        "D'Jasper Probincrux III",
        "Leoz Maxwell Jilliumz",
        "Javaris Jamar Javarison-Lamar",
        "Davoin Shower-Handel",
        "Hingle McCringleberry",
        "L'Carpetron Dookmarriot",
        "J'Dinkalage Morgoone",
        "Xmus Jaxon Flaxon-Waxon",
        "Saggitariutt Jefferspin",
        "D'Glester Hardunkichud",
        "Swirvithan L'Goodling-Splatt",
        "Quatro Quatro",
        "Ozamataz Buckshank",
        "Beezer Twelve Washingbeard",
        "Shakiraquan T.G.I.F. Carter",
        "X-Wing @Aliciousness",
        "Sequester Grundelplith M.D.",
        "Scoish Velociraptor Maloish",
        "T.J. A.J. R.J. Backslashinfourth V",
        "Eeeee Eeeeeeeee",
        "Donkey Teeth",
        "Torque [Construction Noise] Lewith",
        "Tyroil Smoochie-Wallace"
    ]
    bot.say(choose(football))


@plugin.search(r"🍍(|\s)🍕")
def sin(bot, trigger):
    bot.say("This is a sin.")


@plugin.search("xfiles")
@plugin.rate(server=5400)
def xfiles(bot, trigger):
    bot.say("Did you know that the X-Files is going to have 6 new episodes this summer on FOX, Aegisfate?")


@plugin.search("triggered")
def triggered(bot, trigger):
    bot.say(f"{DOMAIN}triggered/{choose(listdir(f'{PATH}triggered'))}")


@plugin.search("to be fair(?!ly)")
def tobefair(bot, trigger):
    bot.say(f"{DOMAIN}v/tobefair.webm")


@plugin.search("stop being poor")
def stopbeingpoor(bot, trigger):
    bot.say(f"{DOMAIN}misc/stopbeingpoor.jpg")


@plugin.search("!tb")
@plugin.command("tb")
def tb(bot, trigger):
    """Spout technobabble. — Can also be triggered with '!tb' anywhere in a message."""
    tb = [
        "When you account for the nm offset variable, the difference between 32-bit and 64-bit CPUs really only matters when calculating differential sub-routine pipeline algorithms.",
        "high 32-bit TOS encrypted voIP",
        "remote access through TeamSpeak",
        "if you reboot it may cement the command scripts that the virus is using to distribute DDOS variants",
        "When the biometrics of the boot sector exceeds the buffer cache then clock-cycles reroute to the LAN thus creating  a load balancing markup stack.",
        "I'll start on a GUI in Visual Basic to backtrack the mainframe.",
        "You can use the ps commands to redirect you to the home directory provided you used the subversion syntax correctly.",
        "The Internet is like water in pipes: when one pipe gets cut the Internet pressure drops because it is leaking uncontrollably from the open pipe. The Internet through WiFi, however, is like a swimming pool. If you open a hole in the building or pool the wifi starts flooding out and the wifi starts to lower. That's the reasoning behind revolving doors. Since they're compartmentalized, the building loses a smaller, fixed amount of internet per entry/exit, which reduces costs and allows more consistency for planning an office's WiFi needs.",
        "I JSON SQL DBs all the time!",
        "Lol you a pussyyyyy when I pull your IP address I'm gonna take your account then you gonna have to make a new account bc you cant get it back",
        "Can't leave without your processor? Clone it! You can copy the processor operating code wirelessly with a sniffer device.",
        "Then they do a triple worm blue cobalt IP hack.",
        "That's how the hacking's done. Satellite telemetry.",
        "SECURITY UPDATES CAUSE AUTISM. WON'T SOMEBODY THINK OF THE CHILDREN???",
        "The asymmetrical phase splitter is offline. We need to compensate for the gravimetric charge imbalance by re-routing power through the electron plasma injector port.",
        "Overheating weak partitions inverts the critical protocols.",
        "Higher numbered ports are always faster, because they travel nearer the outside of the wire, and the 'skin effect' means that that type of transmission is more reliable. So port 80 is going to be slower. If you want to connect with a very fast speed, you might want to try port 3389. This is why when you connect to port 22 you're probably only going to get some kind of text interface, if you connect to port 80 you might get some images along with it, and if you connect to port 3389, you'll get to see and interact with the whole operating system.",
        "That's a node brainer!",
        "Laptops generally don't need to take as many breaks/pauses as desktops, so they don't need that key. Sometimes, the larger laptops like yours w/ a numpad will have it, but only if the laptop hasn't worked out in a while, and gets winded easily.",
        "In order to hack a laptop's battery you need to initiate a GET request from an HTML page then use CSS to parse the DOS command XPLDBTRY.EXE that will make the battery's cooling fail, and then explode.",
        "Atlas Seeds contain zonally-shifted quasi-stellar substrate. WARNING: do not allow matrix to commune with this dimensional space.",
        "Sending packets is reserved to level 1337 hackers only. If you really want to do this you would need to bypass the FireWire's mainframe on your computer. Then you would need to encrypt and enumerate the firewall of whatever server you are trying to send the packet to. Then you would need to exploit the server's hypervisor root code to overflow the VGA interface. After that, all you need to do is code a VPN in Visual Basic and you should be able to do it without any problems.",
        "You should rebuild the kernel but only after rebooting your router. It gets a bit tricky with the buttons 'cause you need to press ctrl + alt + printscreen for 5 seconds and at the same time the reset button on your router. Last time I used my hands for the keyboard and reached for the router with one foot and managed to send the packet, although I also installed a firewall on Winamp and now I can only play Nickelback songs.",
        "Yeah but quantum info extraction was patched by the NSA last month, you gotta entangle the data stream to a local area network loop now.",
        "Don't worry, you'll just need to use a Raspberry Pi to enable four-factor authentication VPN firewalls and he won't be able to get into the mainframe!",
        "Uh oh, his friend is good with Linux! Better watch out! He might grep into your sudoers file and DDoS your hard drive!",
        "We reverse engineered Amazo's operating system and whipped up a virus to wipe his CPU.",
        "He's got a better grasp on Python 6 malware encryption than anybody at the DEO.",
        "I don't want to say the computer is old, but its IP address was 1.",
        "Are you coding in SQL or Java?",
        "Your UI is open-source JPEGs you got from MP3s off the web.",
        "Software running slow? Just decompile it!",
        "The secondary gyrodyne relays of the propulsion field intermatrix have depolarized!",
        "The Enterprise computer system is controlled by three primary main processing cores, cross-linked with a redundant melacortz ramistat. Fourteen kiloquad interface modules. The core element is based on an FTL nanoprocessor with twenty five bilateral kelilactirals, with twenty of those being slaved into the primary heisenfram terminal.",
        "Shunt plasma from the buzzard collectors into the Heisenberg compensators in order to generate sufficient tachyon emissions to disperse neutrino buildup around the warp core, thereby establishing a static warp bubble!",
        "Nanogel. It acts as a quantum transducer.",
        "Don’t forget to move your mouse counter clockwise to reverse the logging process.",
        "But since their cryptographic protocols use poly-phasic entagled waveforms, cracking a code set would take half a century.",
        "If I can just overclock the UNIX django, I can BASIC the DDOS root. Damn. No Dice. But wait...if I disencrypt their kilobytes with a backdoor handshake then...jackpot!",
        f"{DOMAIN}v/Rockwell_Retro_Encabulator.mp4"
    ]
    bot.say(choose(tb), max_messages=2)


@plugin.command("jolly")
@plugin.rate(server=21600)
def jolly(bot, trigger):
    """Nothing tops The Jolly Rancher story.
    Server-wide rate-limit of once every 6 hours."""
    bot.say("Nothing tops the Jolly Rancher story.")
    bot.say("Steve and his girlfriend Samantha went off to college in August. She went to Florida State, he went to Penn. So, she decides to fly to PA to visit him. He was really happy to see her so he decided to give her some oral action.")
    bot.say("He had done this numerous times before and he always enjoyed doing it...but for some reason, this time, she smelled really horrible, and she tasted even worse. He didn't want to offend her though because he hadn't seen her in months...so he put a Jolly Rancher in his mouth to cover it up, even though it didn't do much to help.")
    bot.say("In the course of eating her out, he accidentally pushed the candy inside of her... and stuck a finger in to grab it out. He took it out, and put it back into his mouth and bit it. Only...it wasn't the Jolly Rancher.")
    bot.say("It was a nodule of gonorrhea.")
    bot.say("As in, the blister-like structure that gonorrhea makes filled with diseased pus was the size of a fucking Jolly Rancher and the poor guy BIT it. I guess it was really dark in the room. He freaked out and started vomiting all over the place when it exploded in his mouth...")
    bot.say("He demanded to know what was going on, turns out she had cheated on him at a club like, the first week of college, and fucked some random guy and the stupid bitch had no clue what was wrong with her. She noticed a strange smell though.")
    bot.say("So now, Steve is freaking out that he now has gonorrhea of the mouth and God knows what else.")


@plugin.command("hg")
def hg(bot, trigger):
    """I've got the highground now!"""
    bot.say(f"{DOMAIN}misc/highground.jpg")


@plugin.search("!fgr")
@plugin.command("fgr")
def fgr(bot, trigger):
    """Family Guy reference!!!!!
    Can also be triggered with '!fgr' anywhere in a message."""
    fgr = [
        f"{DOMAIN}fgr/gay.jpg",
        f"{DOMAIN}fgr/gears.jpg",
        f"{DOMAIN}fgr/hang.gif",
        f"{DOMAIN}fgr/stewie-gun.jpg"
    ]
    bot.say(choose(fgr))


@plugin.search("!adr")
@plugin.command("adr")
def adr(bot, trigger):
    """American Dad reference!
    Can also be triggered with '!adr' anywhere in a message."""
    bot.say(f"{DOMAIN}fgr/ADR.jpg")


@plugin.search("!csr")
@plugin.command("csr")
def csr(bot, trigger):
    """Cleveland Show reference!
    Can also be triggered with '!csr' anywhere in a message."""
    bot.say(f"{DOMAIN}fgr/CSR.jpg")


# === NSFW Commands ===
@plugin.search("!!banebread")
def banebread(bot, trigger):
    bot.say(f"{DOMAIN}nsfw/banebread.png")


@plugin.search("!!bread")
def bread(bot, trigger):
    bot.say(f"{DOMAIN}nsfw/🍞.png")


@plugin.search("!!datascii")
def datascii(bot, trigger):
    bot.say(f"{DOMAIN}nsfw/datascii.gif")


@plugin.search("!!dickaroo")
def dickaroo(bot, trigger):
    bot.say(f"{DOMAIN}nsfw/dickaroo.gif")


@plugin.search("!!fgr")
def fgrnsfw(bot, trigger):
    bot.say(f"{DOMAIN}nsfw/chris-in-brian.png")


@plugin.search("!!ghostbabies")
def ghostbabies(bot, trigger):
    bot.say(f"{DOMAIN}nsfw/ghostbabies.gif")


@plugin.search("!!gimp")
def gimp(bot, trigger):
    bot.say(f"{DOMAIN}nsfw/gimp.gif")


@plugin.search("!!nazi")
def nazi(bot, trigger):
    bot.say(f"{DOMAIN}nsfw/nazi.gif")


@plugin.search("!!ponies")
def ponies(bot, trigger):
    bot.say(f"{DOMAIN}nsfw/ponies.mp4")


@plugin.search("!!jordan")
def jordan(bot, trigger):
    bot.say(f"{DOMAIN}jordan/{choose(listdir(f'{PATH}jordan'))}")


@plugin.search("!!cockhunter")
def cock_hunter(bot, trigger):
    bot.say(f"{DOMAIN}nsfw/cock_hunter.webp")


@plugin.search("!!twerk")
def twerk(bot, trigger):
    bot.say(f"{DOMAIN}twerk/{choose(listdir(f'{PATH}twerk'))}")
# === NSFW Commands ===


@plugin.rule("^!b8$")
def beight(bot, trigger):
    bot.say("steam://install/567090")


@plugin.rule(r"^Tasian\sloves\spickles\.($|\s)")
def tasianpickles(bot, trigger):
    bot.say(f"{DOMAIN}tasian/pickles.webp")


@plugin.search("!asg")
@plugin.command("asg")
def allsystemsgo(bot, trigger):
    """Can also be triggered with "!asg" anywhere in a message."""
    bot.say(f"{DOMAIN}misc/asg.webp")


@plugin.search("murica")
@plugin.command("america")
def murica(bot, trigger):
    """Summons Freedom™ into chat.
    Can also be triggered with 'murica' anywhere in a message."""
    bot.say(f"{DOMAIN}murica/{choose(listdir(f'{PATH}murica'))}")


@plugin.search("!knock")
@plugin.command("knock")
def knock(bot, trigger):
    """RP: America knocks on your door...
    Can also be triggered with '!knock' anywhere in a message."""
    bot.say(f"{DOMAIN}murica/knockknock.webp")


@plugin.command("pledge")
@plugin.rate(channel=5400)
def pledge(bot, trigger):
    """Say the United States Pledge of Allegiance.
    Channel-wide rate-limit of 90 minutes."""
    bot.say("I pledge allegiance to the flag of the United States of America. Thank you very very much for letting us little kids live here. It really really was nice of you. You didn't have to do it. And it's really not creepy to have little little kids mindlessly recite this anthem every day and pledge their life to a government before theyre old enough to really think about what they're saying.")
    bot.say("This is not a form of brainwashing. This is not a form of brainwashing. This is not a form of brainwashing.")
    bot.say("This is really the greatest country in the whole world. All the other countries suck. And if this country ever goes to go to war, as its often wont to do, I promise to help go and kill all the other country's kids.")
    bot.say("God bless Johnson & Johnson. God bless GE. God bless Citigroup.")


@plugin.search("mushkin")
@plugin.rate(server=5400)
def mushkin(bot, trigger):
    bot.say("Hey xnaas and feek, did you know that Mushkin announced a 4TB SSD for $500 at CES 2016 and never fuckin' delivered? How neat is that?")


@plugin.command("mirai")
def mirai(bot, trigger):
    """Gone but not forgotten, noble soviet bear."""
    bot.say(f"{DOMAIN}putin/🐻.mp4")


#@plugin.search("!putin")
#@plugin.command("putin")
#def putin(bot, trigger):
#    """Posts a Putin meme of some sort.
#    Can also be triggered with '!putin' anywhere in a message."""
#    putin = [
#        f"{DOMAIN}putin/dance.mp4",
#        f"{DOMAIN}putin/pigeon.mp4",
#        f"{DOMAIN}putin/ritz.gif",
#        f"{DOMAIN}putin/🐻.mp4"
#    ]
#    bot.say(choose(putin))
@plugin.search(r"\bputin\b")
def putin(bot, trigger):
    fuck_putin = [
        "Fuck Putin. All my homies hate Putin.",
        "Putin is a little bitch boy.",
        f"{DOMAIN}putin/pootin.webp"
    ]
    bot.say(choose(fuck_putin))


@plugin.command("aidsclub")
def aidsclub(bot, trigger):
    """Welcome to the club, loser."""
    bot.say(f"{DOMAIN}misc/aidsclub.webp")


@plugin.search("!barometer")
@plugin.command("barometer")
def barometer(bot, trigger):
    """Can also be triggered with '!barometer' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/barometer.webp")


@plugin.rule(r"^Oh,\syou!$")
def ohyou(bot, trigger):
    bot.say(f"{DOMAIN}misc/Oh,you!.jpg")


@plugin.rule("!battletoad")
@plugin.command("battletoad")
def battletoad(bot, trigger):
    """Can also be triggered with '!battletoad' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/battletoad.mp4")


@plugin.search("!beaker")
@plugin.command("beaker")
def beaker(bot, trigger):
    """Can also be triggered with '!beaker' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/beaker.mp4")


@plugin.search("!bomb")
@plugin.command("bomb")
def bomb(bot, trigger):
    """Bombs Japan again... :/
    Can also be triggered with '!bomb' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/bomb.mp4")


@plugin.search("!broden")
@plugin.command("broden")
def broden(bot, trigger):
    """Can also be triggered with '!broden' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/broden.mp4")


@plugin.search("mikey bikey")
def mikeybikey(bot, trigger):
    bot.say(f"{DOMAIN}as/mikeybikey.png")


@plugin.search("meal with it")
def mealwithit(bot, trigger):
    bot.say(f"{DOMAIN}deal/mealwithit.webp")


@plugin.search("deal with it")
def dealwithit(bot, trigger):
    bot.say(f"{DOMAIN}deal/{choose(listdir(f'{PATH}deal'))}")


@plugin.search("!mindjack")
@plugin.command("mindjack")
def mindjack(bot, trigger):
    """Can also be triggered with '!mindjack' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/mindjack.png")


@plugin.command("doge")
@plugin.search("!doge")
def doge(bot, trigger):
    """Doge memes! (There's not very many...)"""
    bot.say(f"{DOMAIN}doge/{choose(listdir(f'{PATH}doge'))}")


@plugin.search("!dogemine")
def dogemine(bot, trigger):
    bot.say(f"{DOMAIN}doge/dogemine.webp")


@plugin.search("!skeledoge")
def skeledoge(bot, trigger):
    bot.say(f"{DOMAIN}doge/skeledoge.webp")


@plugin.search("!batdoge")
def batdoge(bot, trigger):
    bot.say(f"{DOMAIN}doge/batdoge.webp")


@plugin.search("slow down")
def slowdown(bot, trigger):
    bot.say(f"{DOMAIN}a/slowdown.flac")


@plugin.require_admin
@plugin.command("smmcb", "smd")
def smmcb(bot, trigger):
    bot.say(f"{DOMAIN}misc/smmcb.gif")


@plugin.rule("^(noice)$")
def noice(bot, trigger):
    bot.say(trigger.group(1))


@plugin.search("sockbot")
def sockbot(bot, trigger):
    sockbot = [
        f"{DOMAIN}sockbot/headsortails.png",
        f"{DOMAIN}sockbot/knife.png",
        f"{DOMAIN}sockbot/L337.png",
        f"{DOMAIN}sockbot/phone.png",
        "Sockbot: gone, but not forgotten.",
        "Good riddance to Discord, but RIP Sockbot. 😢"
    ]
    bot.say(choose(sockbot))


@plugin.search("!brony")
@plugin.command("brony")
def brony(bot, trigger):
    bot.say(f"{DOMAIN}mike/brony.png")


@plugin.search(r"\bbanned\b")
def banned(bot, trigger):
    bot.say(f"{DOMAIN}banned/{choose(listdir(f'{PATH}banned'))}")


@plugin.search("boycott")
def boycott(bot, trigger):
    bot.say(f"{DOMAIN}misc/boycott.webp")


@plugin.search("censor")
def censor(bot, trigger):
    bot.say(f"{DOMAIN}censored/{choose(listdir(f'{PATH}censored'))}")


@plugin.rule("^(P|B|Ch|D|S|W)ing!$")
def pingpong(bot, trigger):
    bot.say(f"{trigger.group(1)}ong!")


@plugin.rule("^Marco!$")
def marcopolo(bot, trigger):
    bot.say("Polo!")


@plugin.rule("^(W)ee!$")
def weewoo(bot, trigger):
    bot.say(f"{trigger.group(1)}oo!")


@plugin.search("!work")
@plugin.command("work")
def worktoday(bot, trigger):
    """I don't really wanna do the work today..."""
    bot.say(f"{DOMAIN}v/work.webm")


@plugin.search("stbyn")
def stbyn(bot, trigger):
    bot.say(f"Sucks to be you, {italic('nerd')}!")


@plugin.search("🥓")
def bacon(bot, trigger):
    bot.say(f"{DOMAIN}misc/🥓.mp4")


@plugin.search("🍜")
def soupbowl(bot, trigger):
    bot.say(f"{DOMAIN}misc/🍜.mp4")


@plugin.search("🍞")
def breadchan(bot, trigger):
    bot.say(f"{DOMAIN}misc/🍞.png")


@plugin.search("🎅(|🏻|🏼|🏽|🏾|🏿)")
def santa(bot, trigger):
    bot.say(f"{DOMAIN}misc/🎅.png")


@plugin.search("🎧")
def headphones(bot, trigger):
    bot.say(f"{DOMAIN}misc/🎧.png")


@plugin.search("fuck you(?!r)")
def fuckyou(bot, trigger):
    bot.say(f"{DOMAIN}fuck/you/{choose(listdir(f'{PATH}fuck/you'))}")


@plugin.search("(gfy(?!c)|go fuck yourself)")
def gfy(bot, trigger):
    bot.say(f"{DOMAIN}fuck/urself/{choose(listdir(f'{PATH}fuck/urself'))}")


@plugin.rule(r"^What\sthe\sfuck\?$")
def wtfquestion(bot, trigger):
    bot.say(f"{DOMAIN}wtf/wtf¿.gif")


@plugin.rule(r"^What\sthe\sfuck!$")
def wtfexclamation(bot, trigger):
    bot.say(f"{DOMAIN}wtf/wtfh3h3.mp4")


@plugin.rule("^Fuck!$")
def fuckexclamation(bot, trigger):
    bot.say(f"{DOMAIN}fuck/fuck!.webp")


@plugin.rule(r"^Fuck\syeah!$")
def fuckyeah(bot, trigger):
    bot.say(f"{DOMAIN}fuck/fuckyeah!.webp")


@plugin.search(r"\bfuck everything\b")
def fuckeverything(bot, trigger):
    bot.say(f"{DOMAIN}fuck/fuckeverything.webp")


@plugin.search("ftge")
def ftge(bot, trigger):
    ftge = [
        f"{DOMAIN}fuck/ftge-a.webp",
        f"{DOMAIN}fuck/ftge.webp"
    ]
    bot.say(choose(ftge))


@plugin.search("fooled you")
def fooledyou(bot, trigger):
    bot.say(f"{DOMAIN}misc/fooled.png")


@plugin.search("fite me")
def fiteme(bot, trigger):
    bot.say(f"{DOMAIN}fite/{choose(listdir(f'{PATH}fite'))}")


@plugin.rule(r"^Found out I'm gay(|\.|\s)$")
@plugin.rate(channel=21600)
def fagexclamation(bot, trigger):
    bot.say("You're gay. Hey poofta. You're a homo. You're a homo you faggot. Go suck a dick. Go suck a real big dick. Get those dick so far in your mouth that the dick's right there, you got 'em all the way, smashing the back of your throat, balls right there, bangin' on your chin. That's how much I want you to suck dick. Oi. This is me. Pretending to be you. Fist-fuckin' another man in the asshole. Just fist-fuckin' the god-givin' shit out of him. I bet you like that so much you'd like to get fist-fucked while you're doing it. Just getting fist-fucked while you're fist-fuckin' someone else. While you're at it chuck in another one. Just fist-fuckin' two strange men, getting your asshole fist-fucked with someone you just met on Grindr. I bet you wish these were dicks. I bet you wish these were big floppy dicks. You're in a big forest of dicks. Getting dicks all over ya. Covering yourself in cum. Loving cum. Can I suck your dick? Can I suck your dick and then kiss you? Kiss you square on the mouth and then fuck you? Scratch that. Can we make love? Can we make love in my bedroom and then maybe if we connect on more than just a physical level, I'll take you out, I'll introduce you to my mum and my dad and my little sister Jennifer, she's really cool. She's into Goosebumps at the moment. And then maybe we can all go out for dinner together. And they'll really like you because of your cool taste in music and your wonderful dress sense. And then maybe, after confronting their initial misguided preconceptions, my family will come to respect our love for its tangibility. And they'll reject it because of bias or religious and political agendas of hate that have been weaved through the social fabric of hundreds and hundreds of years. FAGGOT!!!", max_messages=6)


@plugin.search("fags")
def fags(bot, trigger):
    bot.say(f"{DOMAIN}faggot/fags.png")


@plugin.search("fag(?!s)")
def faggot(bot, trigger):
    faggot = [
        f"{DOMAIN}faggot/faggot.gif",
        f"{DOMAIN}faggot/oh.gif",
        f"{DOMAIN}faggot/urafaget.png",
        "Faggot!",
        "(/¯◡ ‿ ◡)/¯ ~~~~ Abracadabra, you're a faggot!"
    ]
    bot.say(choose(faggot))


@plugin.rule("^Gay!$")
def gayexclamation(bot, trigger):
    gayexclamation = [
        f"{DOMAIN}gay/!.webp",
        f"{DOMAIN}gay/sayshere.webp",
        f"{DOMAIN}gay/shit.webp"
    ]
    bot.say(choose(gayexclamation))


@plugin.search("everything's fucked")
def everythingsfucked(bot, trigger):
    bot.say(f"{DOMAIN}misc/everythingsfucked.gif")


@plugin.rule(r"^o\sshit.*")
def datboi(bot, trigger):
    bot.say(f"{DOMAIN}oshit/{choose(listdir(f'{PATH}oshit'))}")


@plugin.search("!xmas")
@plugin.command("xmas")
def xmassong(bot, trigger):
    """The only good Christmas song.
    Can also be triggered with '!xmas' anywhere in a message."""
    bot.say(f"{DOMAIN}v/xmas.mp4")


@plugin.search("!swat")
@plugin.command("swat")
def swat(bot, trigger):
    """Summon SWAT into chat.
    Can also be triggered with '!swat' anywhere in a message."""
    bot.say(f"{DOMAIN}v/SWAT.mp4")


@plugin.search("(▫|◽|◻|⬜|▪|◾|◼|⬛|🟥|🟧|🟨|🟩|🟦|🟪|🟫)")
@plugin.rate(channel=5400)
def square(bot, trigger):
    bot.say(f"{DOMAIN}v/square.mp4")


@plugin.command("dblflip")
def dblflip(bot, trigger):
    """Flip two tables...at the same time!"""
    bot.say("┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻")


@plugin.search("bite me")
def bitesback(bot, trigger):
    bot.action(f"bites {trigger.nick}")


@plugin.rule("^Bye!$")
def byebye(bot, trigger):
    bot.say(f"{DOMAIN}misc/BYE!.webp")


@plugin.command("cb")
def clickbait(bot, trigger):
    """Post clickbait into chat."""
    clickbait = [
        "10 celebrities you didn't know were transgender! #11 will shock you!",
        "Was it an alien or something?! Can't wait to find out!",
        "When you read these 19 shocking food facts, you'll never want to eat again!",
        "Think this is a normal shed? Just wait until you see what's inside...",
        "She puts her toilet brush under the seat. Why? It's genius!",
        "Fifty Shades of Grey: #36 took my breath away!",
        "These scientists **TRIPLED** a Janitors IQ! The result will break your heart.",
        "How freeing an escaped convict turned this little boy into a MILLIONAIRE!",
        "What This Man Learned From Having Sex With 365 Guys In One Year"
    ]
    bot.say(choose(clickbait))


@plugin.search("COVID19!")
def windofgod(bot, trigger):
    bot.say(f"{DOMAIN}v/windofgod.webm")


@plugin.search("crossfit")
def crossfit(bot, trigger):
    bot.say(f"{DOMAIN}v/crossfit.webm")


@plugin.rule("^dang$")
def dang(bot, trigger):
    bot.say(f"{DOMAIN}misc/dang.jpg")


@plugin.command("dbc")
def dbc(bot, trigger):
    """Post a Dragonbro Chi comic."""
    bot.say(f"{DOMAIN}dbc/{choose(listdir(f'{PATH}dbc'))}")


@plugin.rule(r"^Deus\svult!$")
def deusvult(bot, trigger):
    bot.say(f"{DOMAIN}v/deusvult.webm")


@plugin.search("fake(!| and gay)")
@plugin.command("fake")
def fake(bot, trigger):
    """For when something is super fake.
    Can also be triggered with 'fake!' or 'fake and gay' anywhere in a message."""
    bot.say(f"{DOMAIN}fake/{choose(listdir(f'{PATH}fake'))}")


@plugin.search("!erect")
@plugin.command("erect")
def erect(bot, trigger):
    """Classic Krieger GIF.
    Can also be triggered with '!erect' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/erect.gif")


@plugin.search("GOAT!")
@plugin.command("goat")
def goat(bot, trigger):
    """Greatest of all time!
    Can also be triggered with 'GOAT!' anywhere in a message."""
    bot.say(f"{DOMAIN}v/GOAT.webm")


@plugin.rule("^hackers$")
@plugin.command("hackers")
def hackers(bot, trigger):
    """Summons the world's two greatest hackers.
    Can also be summoned without the preceeding period/full stop."""
    bot.say(f"{DOMAIN}as/hackers.png")


@plugin.rule("^hue.*")
def hue(bot, trigger):
    bot.say(f"{DOMAIN}hue/{choose(listdir(f'{PATH}hue'))}")


@plugin.rule(r"^I am the machine\.(\s$|$)")
def iamthemachine(bot, trigger):
    bot.say("https://www.youtube.com/watch?v=8PAtFsJY5q0")


@plugin.search("I can't even", "I'm literally can't even")
def icanteven(bot, trigger):
    bot.say(f"{DOMAIN}v/icanteven.webm")


@plugin.rule(r"^I\sship\s(it|that).*")
def ishipit(bot, trigger):
    bot.say(f"{DOMAIN}misc/fedex.webp")


@plugin.search("idgaf")
def idgaf(bot, trigger):
    bot.say(f"{DOMAIN}idgaf/{choose(listdir(f'{PATH}idgaf'))}")


@plugin.search("hugh mungus")
def hughmungus(bot, trigger):
    bot.say(f"{DOMAIN}v/hughmungus.webm")


@plugin.search("IMDABES")
def imdabes(bot, trigger):
    bot.say(f"{DOMAIN}v/IMDABES.webm")


@plugin.search("!JPEG")
@plugin.command("jpeg")
def jpeg(bot, trigger):
    """Do I look like I know what a JPEG is?
    Can also be triggered with '!JPEG' anywhere in a message."""
    bot.say(f"{DOMAIN}v/JPEG.webm")


@plugin.search("!kazoo")
@plugin.command("kazoo")
def kazoo(bot, trigger):
    """Kaaazzzzoooooooooo!!!
    Can also be triggered with '!kazoo' anywhere in a message."""
    bot.say(f"{DOMAIN}v/kazoo.webm")


@plugin.rule("^kill me.*")
def killme(bot, trigger):
    bot.say(f"{DOMAIN}killme/{choose(listdir(f'{PATH}killme'))}")


@plugin.rule(r".*((?<!\w)k(y|m)s(?!\w)|kill\syourself).*")
def kys(bot, trigger):
    kys = [
        f"{DOMAIN}kys/deals.webp",
        f"{DOMAIN}kys/elmo.webp",
        f"{DOMAIN}kys/gift.webp",
        f"{DOMAIN}kys/gta.webp",
        f"{DOMAIN}kys/hang.webp",
        f"{DOMAIN}kys/howto.webp",
        f"{DOMAIN}kys/iGuess.webp",
        f"{DOMAIN}kys/ike.webp",
        f"{DOMAIN}kys/kys.webp",
        f"{DOMAIN}kys/mike-pepe.webp",
        f"{DOMAIN}kys/mike.webp",
        f"{DOMAIN}kys/music.webp",
        f"{DOMAIN}kys/ohhai.webp",
        f"{DOMAIN}kys/pasta.webp",
        f"{DOMAIN}kys/pepe.webp",
        f"{DOMAIN}kys/peter-joe.webp",
        f"{DOMAIN}kys/peter.webp",
        f"{DOMAIN}kys/puft.webp",
        f"{DOMAIN}kys/tried.webp",
        f"{DOMAIN}kys/wendys.webp",
        f"{DOMAIN}kys/window.webp",
        "https://lostallhope.com/"
    ]
    bot.say(choose(kys))


@plugin.search("!music")
def listentomusic(bot, trigger):
    bot.say(f"{DOMAIN}kys/music.webp")


@plugin.rule(r"^oh\shai.*")
def ohhai(bot, trigger):
    bot.say(f"{DOMAIN}kys/ohhai.webp")


@plugin.search("(?<!il)legal!")
@plugin.command("legal")
def legal(bot, trigger):
    """100% totally legal!
    Can also be triggered with 'legal!' anywhere in a message."""
    legal = [
        f"{DOMAIN}misc/👍LEGAL👍.mp4",
        f"{DOMAIN}misc/🕺LEGAL🕺.mp4"
    ]
    bot.say(choose(legal))


@plugin.command("judge")
@plugin.require_chanmsg
def judge(bot, trigger):
    """Judge someone or something."""
    judges = [
        "not guilty! https://p.actionsack.com/misc/not-guilty.png",
        "guilty! https://p.actionsack.com/misc/guilty.png"
    ]
    text = plain(trigger.group(2) or '')
    if not text:
        return bot.reply("I need someone or something to judge!")
    bot.say(f"{text} is {choose(judges)}")


@plugin.rule(r"^wat\b")
def wat(bot, trigger):
    bot.say(f"{DOMAIN}wat/{choose(listdir(f'{PATH}wat'))}")


@plugin.search("✝")
def praisejesus(bot, trigger):
    bot.say("Praise Jesus!")


@plugin.search("Jesus Christ")
def jesuschrist(bot, trigger):
    bot.say("Praise Him!")


@plugin.search("Windows 10")
@plugin.command("w10")
def windowsten(bot, trigger):
    """Windows 10 bad.
    Can also be triggered with 'Windows 10' anywhere in a message."""
    bot.say(f"{DOMAIN}W10/{choose(listdir(f'{PATH}W10'))}")


@plugin.search("!wizard", "wazard")
@plugin.command("wizard")
def wazard(bot, trigger):
    """Hagrid tells you what you are.
    Can also be triggered with '!wizard' or 'wazard' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/wazard.mp4")


@plugin.search("wow!")
@plugin.command("wow")
def wow(bot, trigger):
    """Wow! — Can also be triggered with 'wow!' anywhere in a message."""
    bot.say(f"{DOMAIN}wow/{choose(listdir(f'{PATH}wow'))}")


@plugin.search("whoa(?!mi)")
def whoa(bot, trigger):
    bot.say(f"{DOMAIN}misc/whoa.webp")


@plugin.search("wew lad", "wew!")
@plugin.command("wew")
def wew(bot, trigger):
    """wew lad! — Can also be triggered with 'wew!' or 'wew lad' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/wew.webp")


@plugin.rule(r"^(uh\.\.\.|uh{2,})$")
def uhh(bot, trigger):
    bot.say(f"{DOMAIN}uh/{choose(listdir(f'{PATH}uh'))}")


@plugin.search("swiggity swooty")
def swiggityswooty(bot, trigger):
    bot.say(f"{DOMAIN}swiggityswooty/{choose(listdir(f'{PATH}swiggityswooty'))}")


@plugin.search("praise the sun")
@plugin.command("praise")
def praisethesun(bot, trigger):
    """Praise the Sun!
    Can also be triggered with 'praise the sun' anywhere in a message."""
    bot.say(f"{DOMAIN}v/praisethesun.webm")


@plugin.search("#spam")
def spam(bot, trigger):
    bot.say(f"{DOMAIN}misc/spam.png")


@plugin.search("!son")
@plugin.command("son")
def son(bot, trigger):
    """Posts a "don't talk to me or my son" meme/image.
    Can also be triggered with "!son" anywhere in a message."""
    bot.say(f"{DOMAIN}son/{choose(listdir(f'{PATH}son'))}")


@plugin.rule("^sh{2,}$")
def shh(bot, trigger):
    bot.say(f"{DOMAIN}shh/{choose(listdir(f'{PATH}shh'))}")


@plugin.search("sex robot")
def sexrobot(bot, trigger):
    bot.say(f"{DOMAIN}misc/sexrobot.gif")


@plugin.search("!stickers")
@plugin.command("stickers")
def stickers(bot, trigger):
    """Well-known fact: each sticker on your car adds 5 horsepower.
    Can also be triggered with '!stickers' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/stickers.gif")


@plugin.command("shaved")
def shaved(bot, trigger):
    """xnaas' beautiful shaved leg circa 2011."""
    bot.say(f"{DOMAIN}xnaas/shaved.webp")


@plugin.search("!rimshot")
@plugin.command("rimshot")
def rimshot(bot, trigger):
    """Replies with a 'rimshot' GIF.
    Can also be triggered with '!rimshot' anywhere in a message."""
    bot.say(f"{DOMAIN}rimshot/{choose(listdir(f'{PATH}rimshot'))}")


@plugin.search("!newhouse")
@plugin.command("newhouse")
def newhouse(bot, trigger):
    """Can also be triggered with '!newhouse' anywhere in a message."""
    bot.say(f"{DOMAIN}fecktk/newhouse.webp")


@plugin.search("!drone")
@plugin.command("drone")
def drone(bot, trigger):
    """Summons a drone into chat.
    Can also be summoned with '!drone' anywhere in a message."""
    bot.say(f"{DOMAIN}v/drone.webm")


@plugin.search("!cage")
@plugin.command("cage")
def nickcage(bot, trigger):
    """Summons Nicolas Cage into chat.
    Can also be summoned with '!cage' anywhere in a message."""
    bot.say(f"{DOMAIN}cage/{choose(listdir(f'{PATH}cage'))}")


@plugin.search("!va")
@plugin.command("va")
@plugin.rate(user=900)
def voiceactor(bot, trigger):
    """Quote (or pic!) of a #RealVoiceActor.
    Can only be triggered once per 15 minutes per user.
    Can also be triggered with '!va' anywhere in a message."""
    voice_actor = [
        "You are a pathetic worm... Fight for your scraps... Take your pics haha. I am a true artist and someone that crushes vermin like you in my path. You are a fake and a child with no comprehension of skill nor talent. You are weak... Just like so many... I am pleasure to work with... Unless you cross me or treat me like dirt... Then you will feel my fury... You should have been nice... Now you pay... I am not a pushover... haha... I can make your soul cry and beg for mercy... I am tired of you jerks... I will fight back... Every time...",
        "Give me a break! You guys think you have some freaking special talent that deserves all this damn nonrecognition?! You guys want to get paid to sell and just SPEAK these god damn advertisements! I hate that side of this business! Real voice ACTING is art, it is all the animation and film, it is video games!",
        "It is now a flooded market with all these people who do not have any idea what TRUE ACTING/TALENT is!!! Go do your commercial selling adverts... You can have them... You and your boring ass advertisements are not what makes great voice acting! The true pros are chameleons that shift into new voices and attitudes. You think you can attack me and not feel my sting back!? ACTORS are like gods! We have to convey a true sense of identity.",
        "A real actor has to change emotions and have skills to modulate/shift the voice as elegantly as singers do... I have a large 3 octave vocal range... I also have pitch and tone control too. I worked for it...",
        "Haha, I guess you are right... I HATE doing commercials... I fucking hate them... I rather be able to do 100+ animation and game characters then sell damn cars and products any day... Keep your stupid adverts promos and spots... Seeing how many of you fight over them is sad... I have real talent. Fighting for the scraps of a radio commercial is pathetic.",
        "Now I see why Troy Baker is so arrogant too... You types bring it out in the people with REAL talent. Having the rarest vocal chords, a 3 octave singing range and a good tone is WHAT makes someone good at voice acting... Practicing and having the gift of tricking people into thinking you ARE the character... It takes Range, control, tones, colors, emotions... You have no idea how much YOU lack compared to those such as I...",
        "Maybe the business itself is just stupid now... Keep your stupid 30 secs of voice demo reels... THEY SHOW NOTHING... If you people could really act and convey deep emotions... You would show those off... I know you would.. I also know you would show off all your voices if you had them... Not many can do 100+ variations of characters and tones/pitches/etc...I will stick with my unique approaches... You can all copy each other... Eventually the agents will seek NEW talent with something special and different. you can keep your 30sec-1min demo reels too... I will be the maverick and lead the innovation people like you fail to respect...I rather show some meat on the steak I am selling... keep your 5-6 goofy cartoon voices that EVERYONE does identical and copies! I will keep my rich and detailed characters that are superior. Your attacks did nothing to me... Heh... Your words only gave me strength to carry on... The right agents will see my talents and my determinations... As well as my self-respect/pride... Then they will reap the rewards while you and your kind fight for scraps...",
        "This industry used to filter out those that just wanted an easy job where they spoke and got paid for little to nothing special other than talking... Now its a mess... I challenge anyone to do as many character voices as me... My determination is nothing short of a amazing... By the way... I have no upper teeth either... No denture... Nothing on top to speak as you can so easily... My road is hard but I relish in it's challenge! Yet, the fates can not stop me... I learned to speak almost 99% as good as you all regardless... I cannot be stopped. So... I really have better things to do now, like revel in my craft.",
        "I am pleasure to work with... Unless you cross me or treat me like dirt... Then you will feel my fury... You should have been nice... Now you pay... I am not a pushover... haha... I can make your soul cry and beg for mercy... I am tired of you jerks... I will fight back... Every time... Give me a break! You guys think you have some freaking special talent that deserves all this damn nonrecognition?! You guys want to get paid to sell and just SPEAK these god damn advertisements! I hate that side of this business! Real voice ACTING is art, it is all the animation and film, it is video games!",
        "Yes. I take singing seriously... I used to tonedeaf and have slaved over the oven of dedication for 7 years.",
        "Damn... Why can't people just communicate without being dicks?! This happened before and then I had to unleash all my force upon that stupid fool too! I will not let people talk down to me. Those days are... gone...",
        "I have blonde hair and blue eyes... I was born November 18... Char was born November 17... Has blonde hair... Blue eyes... So... Yes... Char Aznable is my hero... That is not real... Freaking humans are nothing like the citizens of Zeon...",
        "I have nothing to hide. I am not afraid of being naked... Do you think I care what you think of me... I say what I want and I am the person... I am... I could care less what people think of me... I know I have talent and the attacks and doubts people throw my way are just lies and inabilities to see my greatness...",
        "Thank you... This is a nice comment... Maybe these stupid insects and take notes and learn what real hospitality is!?",
        "I am sick of attackers and now I fight back... Years and years I was quiet... Not... This... Time... I am so sick of people that are LESS than human! Just be fucking nice and I wont bring out my soulcrusher! Is that too much to ask?! I feel like I am in some stupid episode of PUNKED!",
        "My animation reel is good. You cannot fool me... You cannot weaken my defenses here... I acted those characters all on the fly and made up the scripts on the fly too... I think they are exceptional... Imagine when I actually TRY to make the proper reels... Why must I keep explaining myself to you narrow minded fools?! I can be such a wonderful and charming man... Yet, now you have made me into the dragon!",
        f"{DOMAIN}misc/'voiceactor'.png"
    ]
    bot.say(choose(voice_actor), max_messages=3)


@plugin.search("!baby")
@plugin.command("baby")
def baby(bot, trigger):
    """Posts an image of GIF involving babies.
    WARNING: not a cutesy command.
    Can also be triggered with '!baby' anywhere in a message."""
    bot.say(f"{DOMAIN}baby/{choose(listdir(f'{PATH}baby'))}")


@plugin.search("boom!")
@plugin.command("boom")
def boom(bot, trigger):
    """BOOM! — Can also be triggered with 'boom!' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/boom.webp")


@plugin.search("burn!")
def burn(bot, trigger):
    bot.say("https://w.wiki/n9f")


@plugin.search("bustin'")
@plugin.command("bustin")
def bustin(bot, trigger):
    """Bustin' makes me feel good!
    Can also be triggered with "bustin'" anywhere in a message."""
    bot.say(f"{DOMAIN}v/bustin.webm")


@plugin.search(r"(?<!s)canned(?!\sair)")
def canned(bot, trigger):
    bot.say(f"{DOMAIN}misc/canned.gif")


@plugin.search(r"consider(\s|ed\s)this")
def consider(bot, trigger):
    bot.say(f"{DOMAIN}misc/consider.webp")


@plugin.search("congraturaisins")
def congraturaisins(bot, trigger):
    bot.say(f"{DOMAIN}misc/congraturaisins.png")


@plugin.search("cowabunga")
def cowabunga(bot, trigger):
    bot.say(f"{DOMAIN}misc/cowabunga.png")


@plugin.search("correct!")
def correcthorse(bot, trigger):
    bot.say(f"{DOMAIN}misc/correct!.gif")


@plugin.search("centaur")
def centaur(bot, trigger):
    bot.say(f"{DOMAIN}misc/centaur.png")


@plugin.search("(?<!rid)(!dance|dance!)")
@plugin.command("dance")
def dance(bot, trigger):
    """Posts a dancing GIF.
    Can also be triggered with 'dance!' or '!dance' anywhere in a message."""
    bot.say(f"{DOMAIN}dance/{choose(listdir(f'{PATH}dance'))}")


@plugin.command("doomanimal")
def doomanimal(bot, trigger):
    """Posts "DOOMANIMAL" video by @andmish."""
    bot.say(f"{DOMAIN}v/DOOMANIMAL.webm")


@plugin.command("doomcrossing")
def doomcrossing(bot, trigger):
    """Posts "DOOM CROSSING: Eternal Horizons" by The Chalkeaters feat. Natalia Natchan."""
    bot.say(f"{DOMAIN}v/DOOMCROSSING.webm")


@plugin.search("doom guy")
def doomguy(bot, trigger):
    bot.say(f"{DOMAIN}misc/doomguy.webp")


@plugin.search("grapist")
def grapist(bot, trigger):
    bot.say(f"{DOMAIN}misc/grapist.gif")


@plugin.search(r"\bit was me\b")
def itwasme(bot, trigger):
    bot.say(f"{DOMAIN}dio/{choose(listdir(f'{PATH}dio'))}")


@plugin.rule(r"^god\sbless\s(.*)")
def godbless(bot, trigger):
    bot.action(f"blesses {trigger.group(1)}")


@plugin.search("hail satan!")
def hailsatan(bot, trigger):
    bot.say(f"{DOMAIN}satan/{choose(listdir(f'{PATH}satan'))}")


@plugin.search("have a seat")
def haveaseat(bot, trigger):
    bot.say(f"{DOMAIN}misc/haveaseat.gif")


@plugin.search("(jews|✡️|✡)")
def jews(bot, trigger):
    bot.say(f"{DOMAIN}jews/{choose(listdir(f'{PATH}jews'))}")


@plugin.rule("^k$")
def kay(bot, trigger):
    kk = [
        "k",
        "👌",
        "👌🏻",
        "👌🏼",
        "👌🏽",
        "👌🏾",
        "👌🏿",
        "👌🏻👌🏼👌🏽👌🏾👌🏿",
        "🆗",
        f"{DOMAIN}k/kermit.mp4",
        f"{DOMAIN}k/seuss.mp4",
        f"{DOMAIN}k/shirt.mp4",
        f"{DOMAIN}k/snow.mp4",
        f"{DOMAIN}k/VHS.mp4",
        f"{DOMAIN}k/vldlk.webp",
        f"{DOMAIN}k/watch.webp"
    ]
    bot.say(choose(kk))


@plugin.search("!words")
def words(bot, trigger):
    # Requested by Aegisfate on 2020-11-19
    bot.say(f"{DOMAIN}misc/words.webp")


@plugin.search("!kiki")
@plugin.command("kiki")
def kiki(bot, trigger):
    """Can also be trigged with '!kiki' anywhere in a message."""
    kiki = [
        f"{DOMAIN}kiki/sauce.png",
        f"{DOMAIN}kiki/snoop.png",
        monospace("[4:44 PM] Kiki: U sound so far right now"),
        "I S M A E L  C H I A  T O R R E S"
    ]
    bot.say(choose(kiki))


@plugin.search("major spoiler")
def majorspoiler(bot, trigger):
    bot.say(f"{DOMAIN}misc/spoiler.png")


@plugin.commands("navy", "navyseal", "seal")
@plugin.rate(server=21600)
def navyseal(bot, trigger):
    """Posts the infamous Navy Seal copypasta...or you get a cat MP4 version.
    Server-wide rate limit of once per 6 hours."""
    navy_seal = [
        f"{DOMAIN}misc/navyseal.mp4",
        "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little ''clever'' comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo."
    ]
    bot.say(choose(navy_seal), max_messages=4)


@plugin.search("racist")
def racist(bot, trigger):
    racists = [
        f"{DOMAIN}racist/birds.gif",
        f"{DOMAIN}racist/blackmexican.gif",
        f"{DOMAIN}racist/fall.gif",
        f"{DOMAIN}racist/nelson.gif",
        f"{DOMAIN}racist/prettyracist.mp4",
        f"{DOMAIN}racist/racist.mp4",
        f"{DOMAIN}racist/shake.gif",
        f"{DOMAIN}racist/wash.png"
    ]
    bot.say(choose(racists))


@plugin.search("nigger")
def niggers(bot, trigger):
    niggers = [
        f"{DOMAIN}racist/nig/cana.png",
        f"{DOMAIN}racist/nig/kan.png",
        f"{DOMAIN}racist/nig/kristen.png",
        f"{DOMAIN}racist/nig/naggers.gif",
        f"{DOMAIN}racist/nig/welfare.png"
    ]
    if trigger.is_privmsg or trigger.sender == "#nsfw":
        bot.say(choose(niggers))


@plugin.search("pasta disasta")
def pastadisasta(bot, trigger):
    bot.say(f"{DOMAIN}🍝/disasta.webm")


@plugin.search("(?<!his)panic!")
def panic(bot, trigger):
    bot.say(f"{DOMAIN}panic/{choose(listdir(f'{PATH}panic'))}")


@plugin.search("my brand")
def mybrand(bot, trigger):
    bot.say(f"{DOMAIN}v/MY_BRAND!.webm")


@plugin.search("!nms")
def nms(bot, trigger):
    bot.say(f"{DOMAIN}nms/{choose(listdir(f'{PATH}nms'))}")


@plugin.rule(r"^(nice|sick)\sgif.*")
def sickgif(bot, trigger):
    bot.say(f"{DOMAIN}misc/sickgif.gif")


@plugin.rule("^nerd!$")
def nerd(bot, trigger):
    bot.say(f"{DOMAIN}misc/nerd!.gif")


@plugin.search("neat!")
def neat(bot, trigger):
    bot.say(f"{DOMAIN}neat/{choose(listdir(f'{PATH}neat'))}")


@plugin.require_admin
@plugin.search("my server")
def myserver(bot, trigger):
    bot.say(f"{DOMAIN}server/{choose(listdir(f'{PATH}server'))}")


@plugin.search(r"(?<!\w)moist(?!\w)")
def moist(bot, trigger):
    bot.say(f"{DOMAIN}moist/{choose(listdir(f'{PATH}moist'))}")


@plugin.search("!manga")
@plugin.command("manga")
def manga(bot, trigger):
    """Posts a clip from the BowserVids "What's in the bag?" video.
    Can also be triggered with '!manga' anywhere in a message."""
    bot.say(f"{DOMAIN}v/manga.mp4")


@plugin.search("LET ME IN")
def letmein(bot, trigger):
    bot.say(f"{DOMAIN}v/letmein.mp4")


@plugin.search("I made this")
def imadethis(bot, trigger):
    bot.say(f"{DOMAIN}OC/{choose(listdir(f'{PATH}OC'))}")


@plugin.search(r"(?<!\w)eat shit")
def frank(bot, trigger):
    bot.say(f"{DOMAIN}misc/frank.gif")


@plugin.search("GTFO")
def gtfo(bot, trigger):
    bot.say(f"{DOMAIN}misc/gtfo.png")


@plugin.search("hawt")
def hawt(bot, trigger):
    bot.say("🥵")


@plugin.rule("^hwat.*")
def hwat(bot, trigger):
    bot.say(f"{DOMAIN}hwat/{choose(listdir(f'{PATH}hwat'))}")


@plugin.search(r"I see you(?!('|r))")
def iseeyou(bot, trigger):
    bot.say(f"{DOMAIN}👀/iSeeU.mp4")


@plugin.search("eyelids")
def eyelids(bot, trigger):
    bot.say(f"{DOMAIN}👀/eyelids.mp4")


@plugin.search("👀")
def eyes(bot, trigger):
    bot.say(f"{DOMAIN}👀/{choose(listdir(f'{PATH}👀'))}")


@plugin.search(r"💩(|\s)💩")
def shit(bot, trigger):
    bot.say(f"{DOMAIN}💩/{choose(listdir(f'{PATH}💩'))}")


@plugin.search("!tesla")
@plugin.command("tesla")
def tesla(bot, trigger):
    """Can also be triggered with '!tesla' anywhere in a message."""
    bot.say(f"{DOMAIN}v/tesla.webm")


@plugin.search("!vn")
@plugin.command("vn")
def vapenaysh(bot, trigger):
    """Vape naysh, y'all!
    Can also be triggered with '!vn' anywhere in a message."""
    bot.say(f"{DOMAIN}vn/{choose(listdir(f'{PATH}vn'))}")


@plugin.search("🦈")
def sharku(bot, trigger):
    bot.say(f"{DOMAIN}🦈/{choose(listdir(f'{PATH}🦈'))}")


@plugin.search(r"🦇(|\s)👨")
@plugin.command("batman")
def batman(bot, trigger):
    """Summons a Batman. Names are base64 encoded.
    Can also be triggered by sending a message that is only the "🦇👨" emoji."""
    bot.say(f"{DOMAIN}🦇👨/{choose(listdir(f'{PATH}🦇👨'))}")


@plugin.search("🤔{3,}")
def think(bot, trigger):
    bot.say(f"{DOMAIN}think/{choose(listdir(f'{PATH}think'))}")


@plugin.search("🚸")
def as_linus(bot, trigger):
    bot.say(f"{DOMAIN}as/linus.png")


@plugin.search("🚬")
def smoking(bot, trigger):
    bot.say(f"{DOMAIN}misc/smoking.webp")


@plugin.search("🚁")
def heli(bot, trigger):
    bot.say(f"{DOMAIN}🚁/{choose(listdir(f'{PATH}🚁'))}")


@plugin.search("🍝")
def spaghetti(bot, trigger):
    bot.say(f"{DOMAIN}🍝/{choose(listdir(f'{PATH}🍝'))}")


@plugin.search("svehla")
def svehla(bot, trigger):
    bot.say(f"{DOMAIN}misc/svehla.webp")


@plugin.search("🗑")
def trash(bot, trigger):
    bot.say(f"{DOMAIN}misc/🗑.webp")


@plugin.search("!cumcan")
@plugin.command("cumcan")
def cumcan(bot, trigger):
    """Can also be triggered with '!cumcan' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/cumcan.webp")


@plugin.search("!cancer")
@plugin.command("cancer")
def cancer(bot, trigger):
    """Warning! Posts pure cancer into chat.
    Can also be triggered with '!cancer' anywhere in a message."""
    cancer_images = [
        f"{DOMAIN}as/cancer-list.png",
        f"{DOMAIN}as/cancer-microscope.png"
    ]
    bot.say(choose(cancer_images))


@plugin.search("!daquan")
@plugin.command("daquan")
def daquan(bot, trigger):
    """Can also be triggered with '!daquan' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/daquan.jpg")


@plugin.search("!heff")
@plugin.command("heff")
def heff(bot, trigger):
    """Is only game, why you heff to be mad?
    Can also be triggered with '!heff' anywhere in a message."""
    bot.say(f"{DOMAIN}v/heff.webm")


@plugin.search("!salty", "🧂")
@plugin.command("salty")
def salty(bot, trigger):
    """Can also be triggered with '!salty' anywhere in a message."""
    bot.say(f"{DOMAIN}salt/{choose(listdir(f'{PATH}salt'))}")


@plugin.search(r"\[laughs\]")
def laughs(bot, trigger):
    bot.say(f"{DOMAIN}misc/laughs.jpg")


@plugin.action_command("raughs")
@plugin.search(r"\[raughs\]")
def raughs(bot, trigger):
    bot.say(f"{DOMAIN}tasian/raughs.webp")


# Action Sack People Section
@plugin.search("!asak")
@plugin.command("asak")
def asak(bot, trigger):
    """Posts an Action Sack meme.
    Can also be triggered with '!asak' anywhere in a message."""
    bot.say(f"{DOMAIN}as/{choose(listdir(f'{PATH}as'))}")


@plugin.search("!bytes")
@plugin.command("bytes")
def ComputersByte(bot, trigger):
    """Posts a ComputersByte meme.
    Can also be triggered with '!bytes' anywhere in a message."""
    bot.say(f"{DOMAIN}bytes/{choose(listdir(f'{PATH}bytes'))}")


@plugin.search("!fecktk")
@plugin.command("fecktk")
@plugin.rate(user=900)
def fecktk(bot, trigger):
    """A user triggering this command can only do so once per 15 minutes."""
    bot.say(f"{DOMAIN}fecktk/{choose(listdir(f'{PATH}fecktk'))}")


@plugin.search("!feek")
@plugin.command("feek")
@plugin.rate(user=900)
def feek(bot, trigger):
    """A user triggering this command can only do so once per 15 minutes."""
    feeks = [
        "Works for Me™",
        f"{DOMAIN}feek/ben.webp",
        f"{DOMAIN}feek/bitch.webp",
        f"{DOMAIN}feek/die.webp",
        f"{DOMAIN}feek/error.webp",
        f"{DOMAIN}feek/feek01.webp",
        f"{DOMAIN}feek/feek02.webp",
        f"{DOMAIN}feek/feek03.webp",
        f"{DOMAIN}feek/feek04.webp",
        f"{DOMAIN}feek/feek05.webp",
        f"{DOMAIN}feek/feek06.webp",
        f"{DOMAIN}feek/feek07.webp",
        f"{DOMAIN}feek/feek08.webp",
        f"{DOMAIN}feek/free.webp",
        f"{DOMAIN}feek/hated.webp",
        f"{DOMAIN}feek/hidden.webp",
        f"{DOMAIN}feek/lucky.webp",
        f"{DOMAIN}feek/PokéKeith.webp",
        f"{DOMAIN}feek/rape.webp"
    ]
    bot.say(choose(feeks))


@plugin.search("!jaja")
@plugin.command("jaja")
@plugin.rate(user=900)
def jajabro(bot, trigger):
    """A user triggering this command can only do so once per 15 minutes."""
    bot.say(f"{DOMAIN}jaja/{choose(listdir(f'{PATH}jaja'))}")


@plugin.search("!kristen")
@plugin.command("kristen")
def kristen(bot, trigger):
    bot.say(f"{DOMAIN}kristen/{choose(listdir(f'{PATH}kristen'))}")


@plugin.search("!mike")
@plugin.command("mike")
@plugin.rate(user=900)
def mike(bot, trigger):
    """A user triggering this command can only do so once per 15 minutes."""
    mikes = [
        f"{DOMAIN}mike/720v1080.png",
        f"{DOMAIN}mike/8ball.png",
        f"{DOMAIN}mike/amnesia.png",
        f"{DOMAIN}mike/bath.png",
        f"{DOMAIN}mike/bernie.png",
        f"{DOMAIN}mike/blowie.png",
        f"{DOMAIN}mike/brony.png",
        f"{DOMAIN}mike/change.png",
        f"{DOMAIN}mike/cocksucker.png",
        f"{DOMAIN}mike/cuppstick.gif",
        f"{DOMAIN}mike/cuppstick.png",
        f"{DOMAIN}mike/dance.mp4",
        f"{DOMAIN}mike/doll.png",
        f"{DOMAIN}mike/down.gif",
        f"{DOMAIN}mike/drink.gif",
        f"{DOMAIN}mike/everydaymike.gif",
        f"{DOMAIN}mike/fraud.png",
        f"{DOMAIN}mike/graphene.png",
        f"{DOMAIN}mike/haloistrash.png",
        f"{DOMAIN}mike/high.png",
        f"{DOMAIN}mike/MAGA.png",
        f"{DOMAIN}mike/mashed-potatoes.png",
        f"{DOMAIN}mike/mike001.png",
        f"{DOMAIN}mike/mike002.png",
        f"{DOMAIN}mike/mike004.png",
        f"{DOMAIN}mike/mike005.png",
        f"{DOMAIN}mike/mike006.png",
        f"{DOMAIN}mike/mike008.png",
        f"{DOMAIN}mike/mike009.png",
        f"{DOMAIN}mike/mike010.png",
        f"{DOMAIN}mike/mike011.png",
        f"{DOMAIN}mike/mike012.png",
        f"{DOMAIN}mike/mike013.png",
        f"{DOMAIN}mike/mike014.png",
        f"{DOMAIN}mike/mike015.png",
        f"{DOMAIN}mike/mike016.png",
        f"{DOMAIN}mike/mike017.png",
        f"{DOMAIN}mike/mike018.png",
        f"{DOMAIN}mike/mike019.png",
        f"{DOMAIN}mike/mike020.png",
        f"{DOMAIN}mike/mike021.png",
        f"{DOMAIN}mike/mike022.png",
        f"{DOMAIN}mike/mike023.png",
        f"{DOMAIN}mike/mike024.png",
        f"{DOMAIN}mike/mike025.png",
        f"{DOMAIN}mike/mike026.png",
        f"{DOMAIN}mike/mike027.png",
        f"{DOMAIN}mike/mike028.png",
        f"{DOMAIN}mike/mike029.png",
        f"{DOMAIN}mike/mike030.png",
        f"{DOMAIN}mike/mike031.png",
        f"{DOMAIN}mike/mike032.png",
        f"{DOMAIN}mike/miker.png",
        f"{DOMAIN}mike/MLP.png",
        f"{DOMAIN}mike/MMM.png",
        f"{DOMAIN}mike/noctua.png",
        f"{DOMAIN}mike/nosex.png",
        f"{DOMAIN}mike/quora.png",
        f"{DOMAIN}mike/simple-mike.png",
        f"{DOMAIN}mike/smurf.png",
        f"{DOMAIN}mike/syria.png",
        f"{DOMAIN}mike/virgin.png",
        f"{DOMAIN}mike/yoj.png",
        f"{DOMAIN}mike/yummy-mike.png",
        f"{DOMAIN}mike/📖/📖+.jpg",
        f"{DOMAIN}mike/📖/📖.gif",
        f"{DOMAIN}mike/📖/📖.jpg",
        f"{DOMAIN}mike/📖/📖🐇.jpg"
    ]
    bot.say(choose(mikes))


@plugin.search("!tasian")
@plugin.command("tasian")
@plugin.rate(user=900)
def tasian(bot, trigger):
    """A user triggering this command can only do so once per 15 minutes."""
    bot.say(f"{DOMAIN}tasian/{choose(listdir(f'{PATH}tasian'))}")


@plugin.search("!viz")
@plugin.command("viz")
@plugin.rate(user=900)
def viz(bot, trigger):
    """A user triggering this command can only do so once per 15 minutes."""
    bot.say(f"{DOMAIN}viz/{choose(listdir(f'{PATH}viz'))}")


@plugin.search("!voodoo")
@plugin.command("voodoo")
def voodoo(bot, trigger):
    """A user triggering this command can only do so once per 15 minutes."""
    voodoos = [
        f"{DOMAIN}voodoo/eggslut.webp",
        f"{DOMAIN}voodoo/eggslut-lq.webp",
        f"{DOMAIN}voodoo/eggslut-smol.webp",
        f"{DOMAIN}voodoo/pewpew.webp",
        "I fantasize about fucking California's earthquake fault line. The dirt, the debris, the thought of the earth quivering under me as I slowly stick my dick into its gaping wide entrance. I keep looking at news stories and getting the firmest erections of my life seeing those beautiful cracks. She's so open and so wanting. Each earthquake is like another whimper just begging for me to take her. The amount of cum I've lost just thinking about thrusting my rod into our beloved planet. Talk about getting my rocks off. Fuck I'm hard."
    ]
    bot.say(choose(voodoos), max_messages=2)


@plugin.search("!xnaas")
@plugin.command("xnaas")
@plugin.rate(user=900)
def xnaas(bot, trigger):
    """A user triggering this command can only do so once per 15 minutes."""
    xnass = [
        f"{DOMAIN}xnaas/animals.webp",
        f"{DOMAIN}xnaas/d3.webm",
        f"{DOMAIN}xnaas/fd.mp4",
        f"{DOMAIN}xnaas/gape.webp",
        f"{DOMAIN}xnaas/iShit.webp",
        f"{DOMAIN}xnaas/mac.webp",
        f"{DOMAIN}xnaas/propain.webp",
        f"{DOMAIN}xnaas/pussy.mp4",
        f"{DOMAIN}xnaas/QotH.webp",
        f"{DOMAIN}xnaas/reality.webp",
        f"{DOMAIN}xnaas/shaved.webp",
        f"{DOMAIN}xnaas/typing.webp",
        f"{DOMAIN}xnaas/vamp.webp",
        f"{DOMAIN}xnaas/victory.webp",
        f"{DOMAIN}xnaas/wesmart.webp",
        f"{DOMAIN}xnaas/xnaas001.webp",
        f"{DOMAIN}xnaas/xnaas002.webp",
        f"{DOMAIN}xnaas/xnaas003.webp",
        f"{DOMAIN}xnaas/xnaas004.webp",
        f"{DOMAIN}xnaas/xnaas005.webp",
        f"{DOMAIN}xnaas/xnaas006.webp",
        f"{DOMAIN}xnaas/xnaas008.webp",
        f"{DOMAIN}xnaas/xnaas009.webp",
        f"{DOMAIN}xnaas/xnaas010.webp",
        f"{DOMAIN}xnaas/xnaas011.webp",
        f"{DOMAIN}xnaas/xnaas012.webp",
        f"{DOMAIN}xnaas/xnaas013.webp",
        f"{DOMAIN}xnaas/xnaas014.webp",
        f"{DOMAIN}xnaas/yeehaw.webp",
        f"{DOMAIN}v/tesla.webm"
    ]
    bot.say(choose(xnass))


@plugin.search("!JTL")
@plugin.command("JTL")
@plugin.rate(user=900)
def JTL(bot, trigger):
    """A user triggering this command can only do so once per 15 minutes."""
    JTL = [
        "JTL thinks he's not 100% gay lol",
        "JTL is addicted to {} 😱".format("\u200B".join("xnaas")),
        "God cries because JTL touches himself at night.",
        "JTL's quote addition is insane. Almost feel bad for the dude.",
        f"{DOMAIN}JTL/bushes.webp",
        f"{DOMAIN}JTL/sendit.webp"
    ]
    bot.say(choose(JTL))


@plugin.search("!nC")
@plugin.command("nC")
@plugin.rate(user=900)
def nC(bot, trigger):
    """A user triggering this command can only do so once per 15 minutes."""
    bot.say(f"{DOMAIN}nC/{choose(listdir(f'{PATH}nC'))}")

# /Action Sack People Section


@plugin.search("!RGB")
@plugin.command("RGB")
def RGB(bot, trigger):
    """Can also be triggered with '!RGB' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/RGB.webp")


@plugin.search("savage!")
def savage(bot, trigger):
    bot.say(f"{DOMAIN}savage/{choose(listdir(f'{PATH}savage'))}")


@plugin.search("🥗")
def salad(bot, trigger):
    bot.say(f"{DOMAIN}misc/🥗.png")


@plugin.search("(?<!t)rickles")
def rickles(bot, trigger):
    bot.say(f"{DOMAIN}misc/rickles.png")


@plugin.rule(r"^(yo|)u\swin.*")
def uwin(bot, trigger):
    bot.say(f"{DOMAIN}misc/uWin.png")


@plugin.rule("^you don't say.*")
def udontsay(bot, trigger):
    bot.say(f"{DOMAIN}misc/yds.png")


@plugin.search("you're too slow")
def urtooslow(bot, trigger):
    bot.say(f"{DOMAIN}sanic/{choose(listdir(f'{PATH}sanic'))}")


@plugin.search("whale rape")
def whalerape(bot, trigger):
    bot.say(f"{DOMAIN}v/whalerape.mp4")


@plugin.search("kwaken")
def kwaken(bot, trigger):
    bot.say(f"{DOMAIN}misc/kwaken.png")


@plugin.search("!KFC")
def kfc(bot, trigger):
    bot.say(f"{DOMAIN}kfc/{choose(listdir(f'{PATH}kfc'))}")


@plugin.search("(?<!en)joy!")
def joy(bot, trigger):
    bot.say(f"{DOMAIN}misc/joy.gif")


@plugin.search("bernie")
def bernii(bot, trigger):
    bot.say(f"{DOMAIN}misc/bernii.webp")


@plugin.search("blumkin")
def blumpkin(bot, trigger):
    bot.say(f"{DOMAIN}misc/blumkin.gif")


@plugin.search("!(chief|halo)")
@plugin.command("chief", "halo")
def chief(bot, trigger):
    """Posts a Master Chief/Halo-related image.
    Can also be triggered with '!chief' or '!halo' anywhere in chat."""
    master_chef = [
        f"{DOMAIN}son/chiefs.webp",
        f"{DOMAIN}son/halo.webp",
        f"{DOMAIN}halo/59bullets.png",
        f"{DOMAIN}halo/anime.png",
        f"{DOMAIN}halo/car.gif",
        f"{DOMAIN}halo/face00.gif",
        f"{DOMAIN}halo/face01.gif",
        f"{DOMAIN}halo/Halo5.png",
        f"{DOMAIN}halo/happening.gif",
        f"{DOMAIN}halo/jaja.png",
        f"{DOMAIN}halo/perfect_game.png",
        f"{DOMAIN}halo/pony.png",
        f"{DOMAIN}halo/skiing.png",
        f"{DOMAIN}halo/what_do_you_think.png",
        f"{DOMAIN}halo/❔.png",
        f"{DOMAIN}halo/🗑.png"
    ]
    bot.say(choose(master_chef))


@plugin.search("!drphil")
@plugin.command("drphil")
def drphil(bot, trigger):
    """Can also be triggered with '!drphil' anywhere in a message."""
    bot.say(f"{DOMAIN}drphil/{choose(listdir(f'{PATH}drphil'))}")


@plugin.search("🌀")
def hurricane(bot, trigger):
    bot.say(f"{DOMAIN}🌀/{choose(listdir(f'{PATH}🌀'))}")


@plugin.search("!pepe")
@plugin.command("pepe")
def pepe(bot, trigger):
    """Posts a rare pepe into chat.
    Can also be triggered with '!pepe' anywhere in a message."""
    bot.say(f"{DOMAIN}pepe/{choose(listdir(f'{PATH}pepe'))}")


@plugin.search("repost")
def repost(bot, trigger):
    bot.say(f"{DOMAIN}repost/{choose(listdir(f'{PATH}repost'))}")


@plugin.command("rip")
def rip(bot, trigger):
    bot.say(f"{DOMAIN}emoji/rip.webp")


@plugin.search("!trump")
@plugin.command("trump")
def trump(bot, trigger):
    """Can also be triggered with '!trump' anywhere in a message."""
    bot.say(f"{DOMAIN}trump/{choose(listdir(f'{PATH}trump'))}")


@plugin.command("downvote")
def downvote(bot, trigger):
    bot.say(f"{DOMAIN}vote/down/{choose(listdir(f'{PATH}vote/down'))}")


@plugin.command("upvote")
def upvote(bot, trigger):
    bot.say(f"{DOMAIN}vote/up/{choose(listdir(f'{PATH}vote/up'))}")


@plugin.search("!apologize")
def apologize(bot, trigger):
    bot.say(f"{DOMAIN}misc/apologize.webp")


@plugin.search("(?<!sh)it's happening")
def happening(bot, trigger):
    its_happening = [
        f"{DOMAIN}halo/happening.gif",
        f"{DOMAIN}misc/happening.gif"
    ]
    bot.say(choose(its_happening))


@plugin.rule("^It's time to stop!$")
def timetostop(bot, trigger):
    bot.say(f"{DOMAIN}🛑/{choose(listdir(f'{PATH}🛑'))}")


@plugin.rule("pepsi")
def pepsi(bot, trigger):
    bot.say(f"{DOMAIN}misc/pepsi.gif")


@plugin.search("terrorist")
def terrorists(bot, trigger):
    bot.say(f"{DOMAIN}misc/terrorist.gif")


@plugin.search("space pants")
def spacepants(bot, trigger):
    space_pants = [
        f"{DOMAIN}misc/spacepants.gif",
        f"{DOMAIN}v/spacepants.mp4"
    ]
    bot.say(choose(space_pants))


@plugin.search("!peep")
@plugin.command("peep")
def peep(bot, trigger):
    """Peep on chat. Can also be triggered with '!peep' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/peep.gif")


@plugin.search("🥒")
def cucumber(bot, trigger):
    bot.say(f"{DOMAIN}misc/🥒.gif")


@plugin.search("krang")
def krang(bot, trigger):
    bot.say(f"{DOMAIN}misc/krang.png")


@plugin.command("reality")
@plugin.rate(server=86400)
def reality(bot, trigger):
    """Lays down a hard reality. Rate-limited to once per day on the server."""
    bot.say(f"{DOMAIN}xnaas/reality.webp")


@plugin.search("mass murder")
@plugin.command("shooting")
def shooting(bot, trigger):
    """Can also be triggered with 'mass murder' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/shooting.gif")


@plugin.search(r"🆒(|\s)🐱")
def coolcat(bot, trigger):
    bot.say(f"{DOMAIN}misc/🆒🐱.png")


@plugin.search("shitpost")
def shitpost(bot, trigger):
    bot.say(f"{DOMAIN}shitpost/{choose(listdir(f'{PATH}shitpost'))}")


@plugin.rule("^No!$")
def no(bot, trigger):
    nonono = [
        f"{DOMAIN}no/00.mp4",
        f"{DOMAIN}no/01.mp4",
    ]
    bot.say(choose(nonono))


@plugin.rule(r"^just\.\.\.no$")
def justno(bot, trigger):
    bot.say(f"{DOMAIN}no/just...no.webp")


@plugin.search("🏇")
def horses(bot, trigger):
    bot.say(f"{DOMAIN}🏇/{choose(listdir(f'{PATH}🏇'))}")


@plugin.search("👽")
def alien(bot, trigger):
    bot.say(f"{DOMAIN}misc/👽.webp")


@plugin.search("😮{3,}")
def gaping_mouth(bot, trigger):
    bot.say(f"{DOMAIN}misc/😮.webp")


@plugin.search("(🕷|🕷️)(?!👨)")
def spider(bot, trigger):
    bot.say(f"{DOMAIN}🕷/{choose(listdir(f'{PATH}🕷'))}")


@plugin.search(r"(🕷|🕷️)(|\s)👨")
@plugin.command("spiderman")
def spiderman(bot, trigger):
    """Can also be triggered with '🕷👨' anywhere in a message."""
    bot.say(f"{DOMAIN}🕷👨/{choose(listdir(f'{PATH}🕷👨'))}")


@plugin.search("shitstorm")
def shitstorm(bot, trigger):
    bot.say(f"{DOMAIN}misc/shitstorm.webp")


@plugin.search("!ts")
@plugin.command("ts")
def teamspeak(bot, trigger):
    """Can also be triggered with '!ts' anywhere in a message."""
    bot.say(f"{DOMAIN}a/teamspeak.ogg")


@plugin.search("!tmf")
@plugin.command("tmf")
def thatsmyfetish(bot, trigger):
    """That's my fetish. ( ͡° ͜ʖ ͡°)
    Can also be triggered with '!tmf' anywhere in a message."""
    bot.say(f"{DOMAIN}misc/tmf.webp")


@plugin.rule("^NDA$")
def nda(bot, trigger):
    bot.say(bold("⚠️ That's ⚠️ some ⚠️ NDA ⚠️ shit ⚠️ right ⚠️ there! ⚠️"))


@plugin.search("darude")
def darude(bot, trigger):
    bot.say(f"{DOMAIN}v/darude.mp4")


@plugin.search("numa")
def numanuma(bot, trigger):
    bot.say(f"{DOMAIN}v/numa.mp4")


@plugin.search("!gems")
@plugin.command("gems")
def gems(bot, trigger):
    """The greatest video game song to ever exist.
    Can also be triggered with '!gems' anywhere in a message."""
    bot.say(f"{DOMAIN}v/gems.mp4")


@plugin.search("explosion!")
def explosion(bot, trigger):
    bot.say(f"{DOMAIN}v/explosion/{choose(listdir(f'{PATH}v/explosion'))}")


@plugin.search("I need a hero")
def ineedahero(bot, trigger):
    bot.say(f"{DOMAIN}v/ineedahero.mp4")


@plugin.search("!MDMA")
@plugin.command("mdma")
def mdma(bot, trigger):
    """Can also be triggered with '!MDMA' anywhere in a message."""
    bot.say(f"{DOMAIN}a/MDMA.flac")


@plugin.search("!albatraoz")
@plugin.command("albatraoz")
def albatraoz(bot, trigger):
    """Can also be triggered with '!albatraoz' anywhere in a message."""
    bot.say(f"{DOMAIN}a/albatraoz.flac")


@plugin.search("!swing")
@plugin.command("swing")
def little_swing(bot, trigger):
    """Can also be triggered with '!swing' anywhere in a message."""
    bot.say(f"{DOMAIN}a/swing.flac")


@plugin.search("!rimg", "rave in my garage") # 'rimg' command taken already, so search only
def rave_in_my_garage(bot, trigger):
    bot.say(f"{DOMAIN}a/RIMG.flac")


@plugin.search("!fun") # not going to reserve 'fun' command
def lsn_fun(bot, trigger):
    bot.say(f"{DOMAIN}a/fun.flac")


@plugin.search("Let it go!")
def let_it_go(bot, trigger):
    bot.say(f"{DOMAIN}v/letitgo.mp4")


@plugin.search("☕")
def coffee(bot, trigger):
    bot.say(f"{DOMAIN}☕/☕.webp")


@plugin.search("this is fine")
def thisisfine(bot, trigger):
    bot.say(f"{DOMAIN}fine/{choose(listdir(f'{PATH}fine'))}")


@plugin.search("efnet")
def efnet(bot, trigger):
    bot.say("EFnet? You mean 'Extremely Fucked Network'?")


@plugin.search(r"Who's that Pok(e|é)mon\?")
def whosthatpokemon(bot, trigger):
    bot.say(f"{DOMAIN}v/whos_that_pokemon.mp4")


@plugin.search("clayman")
def fuck_clayman(bot, trigger):
    bot.say(f"{DOMAIN}rekt/shionXclayman.webp")


@plugin.search("but why")
def but_why(bot, trigger):
    bot.say(f"{DOMAIN}misc/butwhy.webp")


@plugin.rule("^F$")
def pay_respects(bot, trigger):
    bot.action("pays respects")


@plugin.rule("^X$")
def x_to_doubt(bot, trigger):
    bot.action("doubts")


@plugin.search(r"\bpiracy\b")
def piracy(bot, trigger):
    bot.say(f"{DOMAIN}v/piracy.mp4")


@plugin.rule("^🦆$")
def duck_gif(bot, trigger):
    bot.say(f"{DOMAIN}emoji/duck.webp")


@plugin.search("!peacemaker")
def peacemaker(bot, trigger):
    bot.say(f"{DOMAIN}v/peacemaker.mp4")


@plugin.search(r"\bselfie\b")
def selfie(bot, trigger):
    bot.say(f"{DOMAIN}a/selfie.flac")


@plugin.search("!surface")
def surface(bot, trigger):
    bot.say(f"{DOMAIN}a/surface.flac")


@plugin.search(r"\bSOPA\b")
def fuck_sopa(bot, trigger):
    bot.say(f"{DOMAIN}a/FUCK_SOPA.flac")


@plugin.search("shit's on fire( |, )yo")
def shits_on_fire_yo(bot, trigger):
    bot.say(f"{DOMAIN}misc/sofy.webp")


@plugin.search("🦞")
def lobster(bot, trigger):
    bot.say(f"{DOMAIN}v/lobster.mp4")


@plugin.search("friday night")
def friday_nights(bot, trigger):
    bot.say(f"{DOMAIN}v/friday_nights.mp4")
