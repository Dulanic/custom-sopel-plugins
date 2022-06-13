"""
Authors: xnaas (2021-2022+), Nachtalb (2021)
License: The Unlicense (public domain)
"""
import re
import time
from datetime import timedelta
from random import choices
from secrets import choice as choose, randbelow
from sopel import plugin, tools
from sopel.formatting import bold, plain


#############################################
#   ____                    __   _          #
#  / ___|   ___    _ __    / _| (_)   __ _  #
# | |      / _ \  | '_ \  | |_  | |  / _` | #
# | |___  | (_) | | | | | |  _| | | | (_| | #
#  \____|  \___/  |_| |_| |_|   |_|  \__, | #
#                                    |___/  #
#############################################
GCHAN = '#casino'
DB_BANK = 'casino_bank'
DB_TIMELY = 'casino_timely'
DB_GRNDM = 'casino_ground_money'


###############################################################################
#  _____   _                 ____   _                     _                   #
# |_   _| | |__     ___     / ___| | |__     ___    ___  | | __   ___   _ __  #
#   | |   | '_ \   / _ \   | |     | '_ \   / _ \  / __| | |/ /  / _ \ | '__| #
#   | |   | | | | |  __/   | |___  | | | | |  __/ | (__  |   <  |  __/ | |    #
#   |_|   |_| |_|  \___|    \____| |_| |_|  \___|  \___| |_|\_\  \___| |_|    #
#                                                                             #
# This *should* be usable for just about every command in the plugin. It has  #
# logic to check just about every scenario.                                   #
###############################################################################
def casino_check(bot, trigger, targetGroup=None, getBank=None, getBet=None):
    # init None
    bank = bet = target = None

    # channel check first
    if trigger.sender != GCHAN:
        raise Exception(f'`.{trigger.group(1)}` only usable in {GCHAN}')

    # get our target
    if targetGroup == 3:
        target = plain(trigger.group(3) or trigger.nick)
    elif targetGroup == 4:
        target = plain(trigger.group(4) or '')
        if not target:
            raise Exception('I need a target, fool!')
    else:
        target = trigger.nick
    target = tools.Identifier(target)
    if target not in bot.channels[trigger.sender].users:
        raise Exception('Please provide a valid user.')
    if target == bot.nick:
        raise Exception(f'{bot.nick} is not a gambler.')

    # the bet checking bit
    if getBet:
        # huge shout-out to Nachtalb for the meat of this section
        try:
            bet = plain(re.sub("[,'$€]", '', trigger.group(3).lower()))
        except (AttributeError, ValueError):
            raise Exception('I need an amount of money.') 
        if bet == 'all':
            if not getBank:
                raise Exception('You used "all" in an invalid context.')
        elif bet.isdigit():
            bet = int(bet)
        else:
            try:
                match = re.match('([\\d.]+)([ckmbt])', bet, re.IGNORECASE)
                calc = {'c': 1e2, 'k': 1e3, 'm': 1e6, 'b': 1e9, 't': 1e12}
                num, size = match.groups()
                bet = int(float(num) * calc[size])
            except (AttributeError, ValueError):
                raise Exception('I need an amount of money.')

    # check target bank, if needed
    if getBank:
        bank = bot.db.get_nick_value(target, DB_BANK, None)
        if bank is None:
            raise Exception(f'{target} is not a gambler yet.')
        if getBet and bet == 'all':
            bet = bank
        if getBet and (bet > bank):
            raise Exception(
                f'{target} tried to do something they cannot afford lol!')

    # poor broke homies
    if (getBet and getBank) and not bet:
        raise Exception(f'You cannot do $0 transactions, {target}...')

    # return whatever values we got
    variables = [bank, bet, target]
    values = [value for value in variables if value is not None]
    return values


#############################################
#     _          _               _          #
#    / \      __| |  _ __ ___   (_)  _ __   #
#   / _ \    / _` | | '_ ` _ \  | | | '_ \  #
#  / ___ \  | (_| | | | | | | | | | | | | | #
# /_/   \_\  \__,_| |_| |_| |_| |_| |_| |_| #
#                                           #
# The plugin used to have award and take    #
#  commands, but it's much simpler to just  #
#  set the desired value of someone's bank. #
#  Could potentially re-add award/take      #
#  commands fairly easily, though.          #
# There is also a command to totally wipe   #
#  someone's data, just to keep the database#
#  somewhat clean-ish, if you're into that. #
#############################################
# This command is to set someone's balance to whatever is desired.
# There used to be award/take commands, but this seems like the 
#   simpler and better solution overall.
@plugin.command('cset')
@plugin.example('.cset 100 nick')
@plugin.require_admin
def casino_set_bank(bot, trigger):
    try:
        amount, target = casino_check(bot, trigger, 4, False, True)
    except Exception as e:
        return bot.say(str(e))

    bot.db.set_nick_value(target, DB_BANK, amount)
    balance = f'${amount:,}'
    bot.say(f'{target} now has {bold(balance)}')


# This command makes it like a user never existed in the casino.
# Should be merged with 'timelyreset' if that TODO is never done.
@plugin.command('nomoremoney')
@plugin.require_admin
def casino_wipe_user(bot, trigger):
    target = plain(trigger.group(3) or '')
    if not target:
        return bot.reply('I need a user.')
    target = tools.Identifier(target)
    bot.db.delete_nick_value(target, DB_BANK)
    bot.db.delete_nick_value(target, DB_TIMELY)
    bot.say(f'Casino data wiped from existence for: {bold(target)}')


# This command is to reset someone's timely timer so they can timely again.
# TODO: this is a full reset that makes it like they never timely'd. but it
#   should really just set the timer far enough back so that they can timely
#   for the normal amount again.
# PRIORITY: low
@plugin.command('timelyreset')
@plugin.require_admin
@plugin.require_chanmsg(f'{GCHAN} only', True)
def casino_timely_reset(bot, trigger):
    target = plain(trigger.group(3))
    if not target:
        return bot.reply('I need a user.')
    target = tools.Identifier(target)
    if target not in bot.channels[trigger.sender].users:
        return bot.reply('I need a valid user.')
    bot.db.delete_nick_value(target, DB_TIMELY)
    bot.say(f'timely reset for: {bold(target)}')


###################################################################
#  _   _                          ____                   _        #
# | | | |  ___    ___   _ __     / ___|  _ __ ___     __| |  ___  #
# | | | | / __|  / _ \ | '__|   | |     | '_ ` _ \   / _` | / __| #
# | |_| | \__ \ |  __/ | |      | |___  | | | | | | | (_| | \__ \ #
#  \___/  |___/  \___| |_|       \____| |_| |_| |_|  \__,_| |___/ #
###################################################################
# This is a simple bank balance checker.
@plugin.commands('bal', r'\$')
@plugin.example('.bal nick')
def casino_get_bank(bot, trigger):
    try:
        bank, target = casino_check(bot, trigger, 3, True, False)
    except Exception as e:
        return bot.say(str(e))

    balance = f'${bank:,}'
    return bot.say(f'{target} has {bold(balance)}')


# This command inits a user into gambling. Required for anything other than
# `.cset` – no casino_check() because we assume the user is not init'd
@plugin.command('iwantmoney')
def casino_init_user(bot, trigger):
    if trigger.sender != GCHAN:
        return bot.reply(f'`.{trigger.group(1)}` only usable in {GCHAN}')
    verifyPoor = bot.db.get_nick_value(trigger.nick, DB_BANK, None)
    if verifyPoor is None:
        claim = 100
        bot.db.set_nick_value(trigger.nick, DB_BANK, claim)
        return bot.reply(f'Here is ${claim} to get you started.')
    else:
        return bot.reply('Sorry, you are already a gambling addict.')


# This allows a user to give some (or all!) of their money to another user.
@plugin.command('give')
@plugin.example('.give 100 nick')
def casino_give_money(bot, trigger):
    # get data for giver of money
    try:
        user_bank, amount, user = casino_check(bot, trigger, None, True, True)
    except Exception as e:
        return bot.say(str(e))

    # get data for receiver of money
    try:
        target_bank, target = casino_check(bot, trigger, 4, True, False)
    except Exception as e:
        return bot.say(str(e))

    # cancel if user tries to give themselves money
    if target == user:
        return bot.reply("You missed the duping bug lol!")

    # transact the money
    user_bank = user_bank - amount
    target_bank = target_bank + amount
    bot.db.set_nick_value(user, DB_BANK, user_bank)
    bot.db.set_nick_value(target, DB_BANK, target_bank)

    # formatting and output
    user_bal = f'${user_bank:,}'
    target_bal = f'${target_bank:,}'
    gifted_amount = f'${amount:,}'
    msg = f'{user} gifted {gifted_amount} to {target}. '
    msg += f'{user}\'s balance: {bold(user_bal)}. '
    msg += f'{target}\'s balance: {bold(target_bal)}.'
    bot.say(msg)


# 'timely' is one way users can earn money for free
@plugin.command('timely')
def casino_timely(bot, trigger):
    try:
        bank, user = casino_check(bot, trigger, None, True, False)
    except Exception as e:
        return bot.say(str(e))

    # get unix timestamp (float) for right now
    now = time.time()

    timely_check = bot.db.get_nick_value(user, DB_TIMELY, None)
    if not timely_check:
        bot.db.set_nick_value(user, DB_TIMELY, now)
        claim = 100
    elif timely_check:
        timely_check_4h = now - timely_check
        if timely_check_4h >= 14400:
            bot.db.set_nick_value(user, DB_TIMELY, now)
            claim = 25
        else:
            to_timely = 14400 - timely_check_4h
            to_timely = str(timedelta(seconds=round(to_timely)))
            return bot.reply(f'{to_timely} until you can claim again, greedy!')

    newBalance = bank + claim
    bot.db.set_nick_value(user, DB_BANK, newBalance)
    newBalance = f'${newBalance:,}'
    return bot.say(f'{user} claimed ${claim}. New balance: {bold(newBalance)}')


# get casino leaderboard
@plugin.command('lb')
@plugin.rate(user=5)
def casino_leaderboard(bot, trigger):
    if trigger.sender != GCHAN:
        bot.reply(f'`.{trigger.group(1)}` only usable in {GCHAN}')
        return plugin.NOLIMIT

    query =   "SELECT canonical, key, value FROM nick_values a join nicknames "
    query += f"b on a.nick_id = b.nick_id WHERE key='{DB_BANK}' "
    query +=  "ORDER BY cast(value as int) DESC LIMIT 5;"
    lb = bot.db.execute(query).fetchall()
    if not lb:
        return bot.say('No gambling addicts yet!')

    for index, person in enumerate(lb):
        rank = index + 1
        # if rank 1 has $0, then no one has anything
        if rank == 1 and int(person[2]) == 0:
            return bot.say("Ain't nobody got shit!")
        # if a user has $0, they don't belong on the leaderboard
        if int(person[2]) == 0:
            pass
        else:
            name = '\u200B'.join(person[0])
            bot.say(f'{rank}. {name}: ${int(person[2]):,}.')


@plugin.command('pick')
def casino_pick(bot, trigger):
    """Pick up money from the floor of the casino."""
    try:
        bank, user = casino_check(bot, trigger, None, True, False)
    except Exception as e:
        return bot.say(str(e))

    floor = bot.db.get_channel_value(GCHAN, DB_GRNDM, [0, None])

    if not floor[0]:
        insults = [
            'There is no money to pick up, greedy fucker.',
            'Sorry you are poor, but there is no money for you.'
        ]
        return bot.reply(choose(insults))

    if floor[1] == user:
        return bot.reply("You can't pick up the money you dropped, jackass.")

    bot.db.set_channel_value(GCHAN, DB_GRNDM, [0, None])
    newBalance = bank + floor[0]
    bot.db.set_nick_value(user, DB_BANK, newBalance)
    newBalance = bold(f'${newBalance:,}')
    bot.reply(f'Congrats! You picked up ${floor[0]:,}. New balance: {newBalance}')


@plugin.command('drop')
def casino_plant(bot, trigger):
    """Drop some money on the floor of the casino."""
    try:
        bank, bet, user = casino_check(bot, trigger, None, True, True)
    except Exception as e:
        return bot.say(str(e))

    # check if there's already any money on the ground
    floor = bot.db.get_channel_value(GCHAN, DB_GRNDM, [0, None])
    if floor[0]:
        return bot.say('There is already money on the ground.')

    # take from user first
    newBalance = bank - bet
    bot.db.set_nick_value(user, DB_BANK, newBalance)
    
    # drop the money on the ground & identify the dropper
    bot.db.set_channel_value(GCHAN, DB_GRNDM, [bet, user])
    return bot.say(f'Someone dropped ${bet:,} on the ground!')


####################################################################
#   ____      _      __  __   ____    _       ___   _   _    ____  #
#  / ___|    / \    |  \/  | | __ )  | |     |_ _| | \ | |  / ___| #
# | |  _    / _ \   | |\/| | |  _ \  | |      | |  |  \| | | |  _  #
# | |_| |  / ___ \  | |  | | | |_) | | |___   | |  | |\  | | |_| | #
#  \____| /_/   \_\ |_|  |_| |____/  |_____| |___| |_| \_|  \____| #
####################################################################
# TODO: merge casino_betflip() and casino_betoddeven() in some way
#  PRI: low
# TODO: merge a lot of the gambling command code; there's a lot of re-use
#  PRI: verylow
@plugin.command('bf')
@plugin.example('.bf 10 h')
@plugin.rate(user=2)
def casino_betflip(bot, trigger):
    """Wager X amount of money on (h)eads or (t)ails. Winning will net you double your bet."""
    try:
        bank, bet, user = casino_check(bot, trigger, None, True, True)
    except Exception as e:
        return bot.say(str(e))

    # verify user choice
    user_choice = plain(trigger.group(4) or '').lower()
    if not user_choice:
        bot.reply('You need to bet on (h)eads or (t)ails.')
        return plugin.NOLIMIT
    elif user_choice in {'h', 'heads', 't', 'tails'}:
        pass
    else:
        bot.reply('You need to bet on (h)eads or (t)ails.')
        return plugin.NOLIMIT

    # take the user's money first
    spend = bank - bet
    bot.db.set_nick_value(user, DB_BANK, spend)

    # set heads or tails
    if user_choice == 'h':
        user_choice = 'heads'
    if user_choice == 't':
        user_choice = 'tails'

    # flip the coin
    heads_or_tails = ['heads', 'tails']
    flip = choose(heads_or_tails)

    # impact of coin flip
    if flip == user_choice:
        winnings = bet * 2
        newBalance = spend + winnings
        bot.db.set_nick_value(user, DB_BANK, newBalance)
        newBalance = bold(f'${newBalance:,}')
        msg = f'Congrats! The coin landed {flip}. You won ${winnings:,}. '
        msg += f'Your new balance is {newBalance}'
    else:
        newBalance = bold(f'${spend:,}')
        msg = f'Sorry, the coin landed {flip}. You lost ${bet:,}. '
        msg += f'Your new balance is {newBalance}.'

    # stress user with delay
    bot.action('flips a coin...')
    time.sleep(1.5)
    bot.reply(msg)


@plugin.command('oe', 'eo')
@plugin.example('.oe 100 e')
@plugin.rate(user=2)
def casino_betoddeven(bot, trigger):
    """Wager X amount of money on (o)dds or (e)vens. Winning will net you double your bet."""
    try:
        bank, bet, user = casino_check(bot, trigger, None, True, True)
    except Exception as e:
        return bot.say(str(e))

    # verify user choice
    user_choice = plain(trigger.group(4) or '').lower()
    if not user_choice:
        bot.reply('You need to bet on (o)dds or (e)vens.')
        return plugin.NOLIMIT
    elif user_choice in {'o', 'odd', 'odds', 'e', 'even', 'evens'}:
        pass
    else:
        bot.reply('You need to bet on (o)dds or (e)vens.')
        return plugin.NOLIMIT

    # take the user's money first
    spend = bank - bet
    bot.db.set_nick_value(user, DB_BANK, spend)

    # set odds or evens
    if user_choice in {'odd', 'even'}:
        pass
    elif user_choice in {'o', 'odds'}:
        user_choice = 'odd'
    elif user_choice in {'e', 'evens'}:
        user_choice = 'even'

    # roll a number
    roll_num = randbelow(101)
    # determine odd/even
    if (roll_num % 2) == 0:
        roll = 'even'
    else:
        roll = 'odd'

    # impact of roll
    if roll == user_choice:
        winnings = bet * 2
        newBalance = spend + winnings
        bot.db.set_nick_value(user, DB_BANK, newBalance)
        newBalance = bold(f'${newBalance:,}')
        msg = f'I rolled {roll_num} ({roll}). You bet on {user_choice}. '
        msg += f'You won ${winnings:,}! New balance: {newBalance}'
    else:
        newBalance = bold(f'${spend:,}')
        msg = f'I rolled {roll_num} ({roll}). You bet on {user_choice}. '
        msg += f'You lost ${bet:,}. New balance: {newBalance}'

    # stress user with delay
    bot.action('rolls some dice or something...')
    time.sleep(1.5)
    bot.reply(msg)


@plugin.command('br')
@plugin.example('.br 100')
@plugin.rate(user=2)
def casino_betroll(bot, trigger):
    """Bet your money on a random roll from 0-100. Roll payouts:
    0-66: 0x // 67-90: 2x // 91-99: 4x // 100: 10x"""
    try:
        bank, bet, user = casino_check(bot, trigger, None, True, True)
    except Exception as e:
        return bot.say(str(e))

    # take the user's money first
    spend = bank - bet
    bot.db.set_nick_value(user, DB_BANK, spend)

    # roll a number 0-100
    roll = randbelow(101)
    # determine multiplier
    if 0 <= roll <= 66:
        multiplier = 0
    elif 67 <= roll <= 90:
        multiplier = 2
    elif 91 <= roll <= 99:
        multiplier = 4
    elif roll == 100:
        multiplier = 10

    # process winnings
    winnings = bet * multiplier
    newBalance = spend + winnings
    bot.db.set_nick_value(user, DB_BANK, newBalance)
    newBalance = bold(f'${newBalance:,}')

    # conditionals
    if multiplier == 0:
        msg = f'You rolled {roll}. You lost. New balance: {newBalance}'
    elif multiplier in {2, 4}:
        msg = f'You rolled {roll}. You win! {multiplier}x multiplier. '
        msg += f'New balance: {newBalance}'
    elif multiplier == 10:
        msg = f'🎊 Holy shit! You rolled a {roll} which means '
        msg += f'{multiplier}x multiplier! New balance: {newBalance} 🎊'

    # Stress user with delay
    bot.action('rolls some dice or something...')
    time.sleep(1.5)
    bot.reply(msg)


@plugin.command('wheel')
@plugin.example('.wheel 100')
@plugin.rate(user=6)
def casino_wheel(bot, trigger):
    """Spin the wheel of fortune! You must go all-in."""
    try:
        bank, bet, user = casino_check(bot, trigger, None, True, True)
    except Exception as e:
        return bot.say(str(e))

    # user must go all-in
    if bank != bet:
        return bot.reply('You must go all-in for the wheel of fortune.')

    # take the user's money first
    spend = bank - bet
    bot.db.set_nick_value(user, DB_BANK, spend)

    # configure wheel spin directions
    pointer = {
        "↗": 10,
        "→": 7,
        "↘": 6,
        "↓": 5,
        "↙": 4,
        "←": 3,
        "↖": 2,
        "↑": 0
    }

    # get result/multiplier
    result = choices(list(pointer.keys()), weights=[
        2, 8, 8, 8, 8, 8, 8, 50], k=1)[0]
    multiplier = pointer[result]

    # process winnings
    winnings = bet * multiplier
    newBalance = spend + winnings
    bot.db.set_nick_value(user, DB_BANK, newBalance)
    newBalance = bold(f'${newBalance:,}')

    # conditionals
    if multiplier == 0:
        msg = f'The arrow is facing [{result}]. {multiplier}x multiplier. '
        msg += f'You lost. New balance: {newBalance}'
    elif 2 <= multiplier <= 7:
        msg = f'The arrow is facing [{result}]. {multiplier}x multiplier! '
        msg += f'You won! New balance: {newBalance}'
    elif multiplier == 10:
        msg = f'🎊 Holy shit! The arrow is facing [{result}]. '
        msg += f'{multiplier}x multiplier! New balance: {newBalance} 🎊'

    # Stress user with delay
    bot.action('spins the wheel...')
    time.sleep(5)
    bot.action('stops the wheel.')
    bot.reply(msg)


##############################################
#  _____                          _          #
# | ____| __   __   ___   _ __   | |_   ___  #
# |  _|   \ \ / /  / _ \ | '_ \  | __| / __| #
# | |___   \ V /  |  __/ | | | | | |_  \__ \ #
# |_____|   \_/    \___| |_| |_|  \__| |___/ #
##############################################
# Random Money Spawner
# Every 60 minutes:
#   • check if money is already on the ground
#   • randomly spawn money if there isn't any
@plugin.interval(3600)
def casino_rndm(bot):
    # check if there's already any money
    floor = bot.db.get_channel_value(GCHAN, DB_GRNDM, [0, None])

    # if there's no money...
    if not floor[0]:
        roll = randbelow(11)
        if roll == 6:  # choose 6 just because
            floor = [randbelow(91)+10, None]
            bot.db.set_channel_value(GCHAN, DB_GRNDM, floor)
            # TODO: add some randomness to the message to
            #       prevent notifications and botting.
            return bot.say(f'${floor[0]} appeared on the ground.', GCHAN)
        else:
            return
    else:
        return
