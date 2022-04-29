"""
Original author: xnaas (2021)
License: The Unlicense (public domain)
"""
from secrets import choice as choose
from sopel import plugin


@plugin.command("salute")
@plugin.rule("^V$")
@plugin.search("!salute", "rock and stone", "⛏️")
def drg_salute(bot, trigger):
    drg_salutes = [
        "By the beard!",
        "Come on, guys! Rock and Stone!",
        "Did I hear a Rock and Stone?",
        "For Karl!",
        "For Rock and Stone!",
        "If you don't Rock and Stone, you ain't coming home!",
        "Leave no dwarf behind!",
        "Like that! Rock and Stone!",
        "None can stand before us!",
        "Rock and roll!",
        "Rock and roll and Stone!",
        "Rock and Stone!",
        "Rock and Stone, brother!",
        "Rock and Stone, everyone!",
        "Rock and Stone forever!",
        "Rock and Stone in the heart!",
        "Rock and Stone - to the bone!",
        "Rock and Stone...yeeaah!",
        "ROCK......AND.... STONE!",
        "Rock on!",
        "Rock solid!",
        "That's it lads, Rock and Stone!",
        "We are UNBREAKABLE!",
        "We fight for Rock and Stone!",
        "We rock!",
        "Yaaaah, Rock and Stone!"
    ]
    bot.say(choose(drg_salutes))


@plugin.command("toast")
@plugin.search("cheers")
def drg_toast(bot, trigger):
    drg_toasts = [
        "Bottoms up, friends!",
        "Cheers!",
        "Cheers everyone!",
        "Darkness is our friend!",
        "For Karl!",
        "Fortune and glory!",
        "Hell Darkness my old friend!",
        "Karl would approve of this.",
        "Last one to finish is a pointy eared leaf lover!",
        "Long live the dwarves!",
        "May your beards be thick, and your goldsatchels heavy!",
        "Miners! The lowest and the highest!",
        "Nothing will stop us now!",
        "Rock and Stone!",
        "Rock and Stone, to the bone!",
        "Skål!",
        "Teamwork and beer will keep us together!",
        "To a successful mission!",
        "To danger!",
        "To darkness!",
        "To gold!",
        "To Karl!",
        "To mates, to darkness, and to making it back alive!",
        "To our continue survival! ...Yeah, right, hahahah!",
        "To Rock and Stone!",
        "To teamwork!",
        "To the Empires of Old!",
        "To the fallen!",
        "To those we lost!"
    ]
    bot.say(choose(drg_toasts))


@plugin.search("karl")
def karl(bot, trigger):
    karls = [
        "This one's for Karl!",
        "For Karl!",
        "To Karl!",
        "That thing ate bullets, like Karl drank beers!",
        "We got it! Karl would be proud!",
        "By Karl! Look at all that pretty sparkly...!",
        "Karl would approve of this.",
        "(drunk) ...K...Karl? Is...is that you?",
        "(drunk) Wait a minute...If all truths are knowable, then all truths must in fact be known.....but by whom? ...Karl would know!",
        "(drunk) I......I.......I know where Karl is! It's so bloody obvious! What...uhhh....hmmm....anyone up for playing the hoop game?",
        "Hmm...what Karl would choose?",
        "I'm gonna wear this in honor of Karl!",
        "People ask why we remember Karl. People ask what made him a legend. Rumor has it Skull Crusher Ale is at least partly to blame. Make of that what you will. Beware."
    ]
    bot.say(choose(karls))
