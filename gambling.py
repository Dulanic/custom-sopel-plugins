from sopel import plugin, tools
from sopel.formatting import bold, italic, plain
from datetime import datetime, timedelta
import random
import re
import secrets
import sqlite3
import time
import unicodedata


GCHAN = "#casino"


# Various Gambling Checks
def gambling_checks(bot, trigger):
    # Set keys to None for checks
    data = {"bet": None, "msg": None, "target": None}

    # Channel Checker – perhaps make this configurable in the future
    if trigger.sender == GCHAN:
        pass
    else:
        data["msg"] = "This command can only be used in {}".format(GCHAN)
        return data

    # Target Check
    # NOTE: This is not near as "universal" as originally thought out...
    #     Could definitely use some improvement in the future.
    # PROBLEM: This code is basically useless for all of the
    #     actual gambling commands. Unfortunately, just swapping
    #     trigger.group(4) and trigger.nick comes with another set of
    #     issues to deal with.
    target = plain(trigger.group(4) or trigger.nick)
    if not target:
        data["msg"] = "If you're seeing this message...everything is horribly broken."
        return data
    if target == bot.nick:
        data["msg"] = "I just run the place; I don't participate."
        return data
    data["target"] = tools.Identifier(target)

    # "Bet" Parsing and Checking
    # We're calling everything a "bet" for simplicity.
    # Many commands below don't involve betting.
    try:
        bet = plain(trigger.group(3).replace(",", "").replace("$", ""))
        if bet.isdigit():
            data["bet"] = int(bet)
    except AttributeError:
        bet = None
    if not bet:
        data["msg"] = "I need an amount of money."
        return data
    else:
        try:
            # Checks for bets made with letters
            # Large thanks to @Nachtalb
            match = re.match("([\\d.]+)([ckmbt])", bet, re.IGNORECASE)
            # TODO: should be some logic for "all" bet
            calc = {
                "C": 1e2, "c": 1e2,
                "K": 1e3, "k": 1e3,
                "M": 1e6, "m": 1e6,
                "B": 1e9, "b": 1e9,
                "T": 1e12, "t": 1e12
            }
            num, size = match.groups()
            data["bet"] = int(float(num) * calc[size])
        except (AttributeError, ValueError):
            data["msg"] = "I need an amount of money."
            return data

    # return keys: 'msg', 'target', and 'bet'
    return data


@plugin.require_admin
@plugin.require_chanmsg
@plugin.command("award")
def award_money(bot, trigger):
    """Bot admin uses the power of Admin Abuse to spawn money from nothing."""
    try:
        data = gambling_checks(bot, trigger)
    except Exception as msg:
        return bot.reply(msg)

    amount = data["bet"]
    msg = data["msg"]
    target = data["target"]

    if not amount:
        return bot.reply(msg)

    # Check for valid target to award money to.
    if target not in bot.channels[trigger.sender].users:
        return bot.reply("Please provide a valid user.")

    new_balance = bot.db.get_nick_value(target, "currency_amount", 0) + amount
    bot.db.set_nick_value(target, "currency_amount", new_balance)
    balance = "${:,}".format(new_balance)
    bot.say("{} now has {}".format(target, bold(balance)))


@plugin.require_admin
@plugin.require_chanmsg
@plugin.command("take")
def take_money(bot, trigger):
    """Bot admin takes (deletes) X amount of money from a user."""
    try:
        data = gambling_checks(bot, trigger)
    except Exception as msg:
        return bot.reply(msg)

    amount = data["bet"]
    msg = data["msg"]
    target = data["target"]

    if not amount:
        return bot.reply(msg)

    # Check for valid target to take money from.
    if target not in bot.channels[trigger.sender].users:
        return bot.reply("Please provide a valid user.")

    new_balance = bot.db.get_nick_value(target, "currency_amount", 0) - amount
    bot.db.set_nick_value(target, "currency_amount", new_balance)
    balance = "${:,}".format(new_balance)
    bot.say("{} now has {}".format(target, bold(balance)))


@plugin.require_chanmsg
@plugin.command("give")
def give_money(bot, trigger):
    """Give X amount of your money to another user."""
    try:
        data = gambling_checks(bot, trigger)
    except Exception as msg:
        return bot.reply(msg)

    amount = data["bet"]
    msg = data["msg"]
    target = data["target"]
    giver = trigger.nick

    if not amount:
        return bot.reply(msg)

    if giver == target:
        return bot.reply("You gifted yourself the same amount, I guess?")

    # Check if the transaction can even occur
    give_check = bot.db.get_nick_value(giver, "currency_amount")
    receive_check = bot.db.get_nick_value(target, "currency_amount")

    if give_check is None:
        return bot.reply(
            "You can't do that yet. Please run `.iwantmoney` first.")

    if receive_check is None:
        return bot.reply(
            "{0} hasn't participated yet. {0} needs to run `.iwantmoney` first.".format(target))

    if amount > give_check:
        return bot.reply(
            "You don't have enough money to complete this transcation, you filthy poor.")

    # Check for valid target to give money to.
    if target not in bot.channels[trigger.sender].users:
        return bot.reply("Please provide a valid user.")

    giver_new_balance = bot.db.get_nick_value(
        giver, "currency_amount", 0) - amount
    target_new_balance = bot.db.get_nick_value(
        target, "currency_amount", 0) + amount
    # Take away the money from the giver.
    bot.db.set_nick_value(giver, "currency_amount", giver_new_balance)
    # Give the money to the target/reciever.
    bot.db.set_nick_value(target, "currency_amount", target_new_balance)
    giver_balance = "${:,}".format(giver_new_balance)
    target_balance = "${:,}".format(target_new_balance)
    gifted_amount = "${:,}".format(amount)
    bot.say(
        "{} gifted {} to {}. {} now has {} and {} has {}.".format(
            giver,
            bold(gifted_amount),
            target,
            giver,
            bold(giver_balance),
            target,
            bold(target_balance)))


@plugin.require_admin
@plugin.command("nomoremoney")
def delete_money(bot, trigger):
    """Bot admin can make it so a user never had any money."""
    # We want to be able to delete money regardless of any checks.
    # Could be the user is gone from the server/channel.
    target = trigger.group(3)

    if not target:
        return bot.reply("I need someone's wealth to eliminate.")

    target = tools.Identifier(target)

    bot.db.delete_nick_value(target, "currency_amount")
    bot.db.delete_nick_value(target, "currency_timely")
    bot.say("{}'s wealth has been deleted from existence.".format(target))


@plugin.command(r"\$")
@plugin.require_chanmsg
def check_money(bot, trigger):
    """Check how much money you or another user has."""
    # We're not using gambling_checks() because it's
    # tuned for most other commands in this plugin.
    # Channel Check
    if trigger.sender == GCHAN:
        pass
    else:
        return bot.reply("This command can only be used in {}".format(GCHAN))

    # Target Check
    target = plain(trigger.group(3) or trigger.nick)
    if not target:
        return bot.reply(
            "If you're seeing this message...everything is horribly broken.")

    target = tools.Identifier(target)

    if target == bot.nick:
        return bot.reply("I just run the place; I don't participate.")
    if target not in bot.channels[trigger.sender].users:
        return bot.reply("Please provide a valid user.")

    # Actual Currency Check
    currency_amount = bot.db.get_nick_value(target, "currency_amount")
    if currency_amount is not None:
        balance = "${:,}".format(currency_amount)
        bot.say("{} has {}".format(target, bold(balance)))
    else:
        bot.say("{} needs to run `.iwantmoney` first.".format(target))


@plugin.require_chanmsg
@plugin.command("iwantmoney")
def init_money(bot, trigger):
    """Use this command to get money for the first time ever and participate in gambling and other fun activities!"""
    # We're not using gambling_checks() because it's
    # tuned for most other commands in this plugin.
    # Channel Check
    if trigger.sender == GCHAN:
        pass
    else:
        return bot.reply("This command can only be used in {}".format(GCHAN))

    target = trigger.nick

    check_for_money = bot.db.get_nick_value(target, "currency_amount")
    if check_for_money is None:
        bot.db.set_nick_value(target, "currency_amount", 100)
        bot.say(
            "Congratulations! Here's {} to get you started, {}.".format(
                bold("$100"), target))


@plugin.require_chanmsg  # Forcing public claiming serves as a reminder to all.
@plugin.command("timely")
def claim_money(bot, trigger):
    """Claim $50 every 12 hours. ($100 for first claim!)"""
    # We're not using gambling_checks() because it's
    # tuned for most other commands in this plugin.
    # Channel Check
    if trigger.sender == GCHAN:
        pass
    else:
        return bot.reply("This command can only be used in {}".format(GCHAN))

    target = trigger.nick

    check_for_money = bot.db.get_nick_value(target, "currency_amount")
    if check_for_money is None:
        return bot.reply(
            "You can't do this yet! Please run the `.iwantmoney` command.")

    now = time.time()

    check_for_timely = bot.db.get_nick_value(target, "currency_timely")
    if check_for_timely is None:
        bot.db.set_nick_value(target, "currency_timely", now)
        claim = check_for_money + 100
        bot.db.set_nick_value(target, "currency_amount", claim)
        balance = "${:,}".format(claim)
        return bot.reply(
            "Here's $100. New balance: {}. Don't forget to claim again in 12 hours! ($50/12h going forward.)".format(bold(balance)))

    check_12_hour = now - check_for_timely
    if check_12_hour >= 43200:
        bot.db.set_nick_value(target, "currency_timely", now)
        claim = check_for_money + 50
        bot.db.set_nick_value(target, "currency_amount", claim)
        balance = "${:,}".format(claim)
        return bot.reply(
            "Here's $50. New balance: {}. Don't forget to claim again in 12 hours!".format(
                bold(balance)))
    else:
        to_12_hour = 43200 - check_12_hour
        time_remaining = str(timedelta(seconds=round(to_12_hour)))
        bot.reply("{} until you can claim again, greedy!".format(time_remaining))


@plugin.command("timelyreset")
@plugin.require_chanmsg
@plugin.require_admin
def timely_reset(bot, trigger):
    """Reset a user's timely timer for whatever reason."""
    target = trigger.group(3)

    if not target:
        return bot.reply("I need someone's timely timer to reset.")

    target = tools.Identifier(target)
    if target not in bot.channels[trigger.sender].users:
        return bot.reply("Please provide a valid user.")

    bot.db.delete_nick_value(target, "currency_timely")
    bot.say("{}'s timely timer has been reset.".format(target))


@plugin.command("betflip", "bf")
@plugin.example(".bf 10 h")
def gamble_betflip(bot, trigger):
    """Wager X amount of money on (h)eads or (t)ails. Winning will net you double your bet."""
    try:
        data = gambling_checks(bot, trigger)
    except Exception as msg:
        return bot.reply(msg)

    bet = data["bet"]
    msg = data["msg"]
    gambler = trigger.nick

    if not bet:
        return bot.reply(msg)

    # Check if user has enough money to make the gamble...
    bet_check = bot.db.get_nick_value(gambler, "currency_amount")
    if bet_check is None:
        return bot.reply(
            "You can't gamble yet! Please run the `.iwantmoney` command.")
    if bet > bet_check:
        return bot.reply(
            "You don't have enough money to make this bet. Try a smaller bet.")

    # Check if user has actually bet (H)eads or (T)ails.
    user_choice = plain(trigger.group(4) or '')
    if not user_choice:
        return bot.reply("You need to bet on (h)eads or (t)ails.")
    if user_choice in ["h", "t", "heads", "tails"]:
        pass
    else:
        return bot.reply("You need to bet on (h)eads or (t)ails.")

    # Take the user's money before continuing
    spend_on_bet = bet_check - bet
    bot.db.set_nick_value(gambler, "currency_amount", spend_on_bet)

    # Set heads or tails
    if user_choice == "h":
        user_choice = "heads"
    if user_choice == "t":
        user_choice = "tails"

    # Flip coin and complete transaction
    heads_or_tails = ["heads", "tails"]
    flip_result = secrets.choice(heads_or_tails)

    if flip_result == user_choice:
        winnings = bet * 2
        new_balance = spend_on_bet + winnings
        bot.db.set_nick_value(gambler, "currency_amount", new_balance)
        balance = "${:,}".format(new_balance)
        msg = "Congrats; the coin landed on {}. You won ${:,}! Your new balance is {}.".format(
            flip_result, winnings, bold(balance))
    else:
        balance = "${:,}".format(spend_on_bet)
        msg = "Sorry, the coin landed on {}. You lost ${:,}. Your new balance is {}.".format(
            flip_result, bet, bold(balance))

    # Stress user with delay
    bot.action("flips a coin...")
    time.sleep(1.5)
    bot.reply(msg)


@plugin.command("br", "betroll")
@plugin.example(".br 200")
def gamble_betroll(bot, trigger):
    """Bet your money on a random roll from 0-100. Roll payouts:
    0-66: 0x // 67-90: 2x // 91-99: 4x // 100: 10x"""
    try:
        data = gambling_checks(bot, trigger)
    except Exception as msg:
        return bot.reply(msg)

    bet = data["bet"]
    msg = data["msg"]
    gambler = trigger.nick

    if not bet:
        return bot.reply(msg)

    # Check if user has enough money to make the gamble...
    bet_check = bot.db.get_nick_value(gambler, "currency_amount")
    if bet_check is None:
        return bot.reply(
            "You can't gamble yet! Please run the `.iwantmoney` command.")
    if bet > bet_check:
        return bot.reply(
            "You don't have enough money to make this bet. Try a smaller bet.")

    # Take the user's money before continuing
    spend_on_bet = bet_check - bet
    bot.db.set_nick_value(gambler, "currency_amount", spend_on_bet)

    # Roll a number 0-100
    roll = secrets.randbelow(101)
    # Determine multiplier
    if 0 <= roll <= 66:
        multiplier = 0
    elif 67 <= roll <= 90:
        multiplier = 2
    elif 91 <= roll <= 99:
        multiplier = 4
    elif roll == 100:
        multiplier = 10

    # Process winnings
    winnings = bet * multiplier
    new_balance = spend_on_bet + winnings
    bot.db.set_nick_value(gambler, "currency_amount", new_balance)
    balance = "${:,}".format(new_balance)

    # Conditionals
    if multiplier == 0:
        msg = "You rolled {}. You lost. {}x multiplier. New balance: {}.".format(
            roll, multiplier, bold(balance))
    elif multiplier in (2, 4):
        msg = "You rolled {}. You win! {}x multiplier. New balance: {}.".format(
            roll, multiplier, bold(balance))
    elif multiplier == 10:
        msg = "🎊 Holy shit! You rolled a {} which means {}x multiplier! New balance: {}. 🎊".format(
            roll, multiplier, bold(balance))

    # Stress user with delay
    bot.say(italic("Rolling a number..."))
    time.sleep(1.5)
    bot.reply(msg)


@plugin.command("oe", "eo")
@plugin.example(".oe 10 e")
def gamble_oddsevens(bot, trigger):
    """Wager X amount of money on (o)dds or (e)vens. Winning will net you double your bet."""
    try:
        data = gambling_checks(bot, trigger)
    except Exception as msg:
        return bot.reply(msg)

    bet = data["bet"]
    msg = data["msg"]
    gambler = trigger.nick

    if not bet:
        return bot.reply(msg)

    # Check if user has enough money to make the gamble...
    bet_check = bot.db.get_nick_value(gambler, "currency_amount")
    if bet_check is None:
        return bot.reply(
            "You can't gamble yet! Please run the `.iwantmoney` command.")
    if bet > bet_check:
        return bot.reply(
            "You don't have enough money to make this bet. Try a smaller bet.")

    # Check if user has actually bet (o)dds or (e)vens.
    user_choice = plain(trigger.group(4) or '')
    if not user_choice:
        return bot.reply("You need to bet on (o)dds or (e)vens.")
    if user_choice in ["o", "e", "odd", "even", "odds", "evens"]:
        pass
    else:
        return bot.reply("You need to bet on (o)dds or (e)vens.")

    # Take the user's money before continuing
    spend_on_bet = bet_check - bet
    bot.db.set_nick_value(gambler, "currency_amount", spend_on_bet)

    # Set odds or evens
    if user_choice in ("odd", "even"):
        pass
    elif user_choice in ("o", "odds"):
        user_choice = "odd"
    elif user_choice in ("e", "evens"):
        user_choice = "even"

    # Roll and complete transaction
    roll_num = secrets.randbelow(101)
    if (roll_num % 2) == 0:
        roll = "even"
    else:
        roll = "odd"

    if roll == user_choice:
        winnings = bet * 2
        new_balance = spend_on_bet + winnings
        bot.db.set_nick_value(gambler, "currency_amount", new_balance)
        balance = "${:,}".format(new_balance)
        msg = "I rolled {}. That's {}. You bet on {}. You won ${:,}! Your new balance is {}.".format(
            roll_num, roll, user_choice, winnings, bold(balance))
    else:
        balance = "${:,}".format(spend_on_bet)
        msg = "I rolled {}. That's {}. You bet on {}. You lost ${:,}. Your new balance is {}.".format(
            roll_num, roll, user_choice, bet, bold(balance))

    # Stress user with delay
    bot.action("rolls a bunch of dice or something...")
    time.sleep(1.5)
    bot.reply(msg)


@plugin.command("wheeloffortune", "wheel")
@plugin.example(".wheel 100")
def gamble_wheel(bot, trigger):
    """Spin the Wheel of Fortune!"""
    try:
        data = gambling_checks(bot, trigger)
    except Exception as msg:
        return bot.reply(msg)

    bet = data["bet"]
    msg = data["msg"]
    gambler = trigger.nick

    if not bet:
        return bot.reply(msg)

    # Check if user has enough money to make the gamble...
    bet_check = bot.db.get_nick_value(gambler, "currency_amount")
    if bet_check is None:
        return bot.reply(
            "You can't gamble yet! Please run the `.iwantmoney` command.")
    if bet > bet_check:
        return bot.reply(
            "You don't have enough money to make this bet. Try a smaller bet.")

    # Take the user's money before continuing
    spend_on_bet = bet_check - bet
    bot.db.set_nick_value(gambler, "currency_amount", spend_on_bet)

    # Configure Wheel Spin Directions
    wheel_direction = ["֎", "֍"]
    pointer_direction = {
        "↗": 7,
        "→": 6,
        "↘": 5,
        "↓": 4,
        "↙": 3,
        "←": 2,
        "↖": 1,
        "↑": 0
    }

    # Get the result first
    wheel_result = random.choices(list(pointer_direction.keys()), weights=[
                                  0.1, 0.4, 0.5, 1, 3, 25, 30, 40], k=1)[0]
    multiplier = pointer_direction[wheel_result]

    # Calculate winnings and award the user
    winnings = bet * multiplier
    new_balance = spend_on_bet + winnings
    bot.db.set_nick_value(gambler, "currency_amount", new_balance)
    balance = "${:,}".format(new_balance)

    # Conditionals
    if multiplier == 0:
        msg = "The arrow is facing [{}]. {}x multiplier. You lost. New balance: {}.".format(
            wheel_result, multiplier, bold(balance))
    elif multiplier == 1:
        msg = "The arrow is facing [{}]. {}x multiplier. Same balance: {}.".format(
            wheel_result, multiplier, bold(balance))
    else:
        msg = "The arrow is facing [{}]. You won: {}x your money! (${:,}). Your new balance is: {}.".format(
            wheel_result, multiplier, winnings, bold(balance))

    # Stress user with delay
    bot.action(
        "spins the wheel...{0}{0}{0}".format(
            secrets.choice(wheel_direction)))
    time.sleep(4)
    bot.say(italic("The wheel slows to a stop..."))
    time.sleep(2)
    bot.reply(msg)


@plugin.command("lb")
@plugin.rate(user=5)
@plugin.require_chanmsg
def gamble_leadboard(bot, trigger):
    """Posts the top 5 richest gamblers."""
    if trigger.sender == GCHAN:
        pass
    else:
        return bot.reply("This command can only be used in {}".format(GCHAN))

    """
    try:
        # Connect to DB
        con = sqlite3.connect("/home/xnaas/sackbot2/sopel/default.db")
        # Create whatever the fuck a cursor is
        cur = con.cursor()
        # SQL Query
        cur.execute("SELECT canonical, key, value FROM nick_values a join nicknames b on a.nick_id = b.nick_id WHERE key='currency_amount' ORDER BY cast(value as int) DESC;")
        # Store results
        lb_base = cur.fetchall()
        # Close db connection
        con.close()
    except sqlite3.OperationalError:
        return bot.reply(
            "Error querying database...most likely no one has gambled yet. Try `.iwantmoney` to get started.")
    """

    # Do it through Sopel, not SQL
    # Need to add back error handling later
    lb_base = bot.db.execute(
        "SELECT canonical, key, value FROM nick_values a join nicknames b on a.nick_id = b.nick_id WHERE key='currency_amount' ORDER BY cast(value as int) DESC;")

    # go through db for results
    for index, person in enumerate(lb_base):
        # Rank/Index required to actually go through data
        rank = index + 1

        # If rank 1 has $0, then no one has anything
        if rank == 1 and int(person[2]) == 0:
            return bot.say("Ain't nobody got shit!")

        # If a user has $0, they don't belong on the leaderboard
        if int(person[2]) == 0:
            pass
        else:
            # print results
            bot.say(
                "{}. {}: ${:,}.".format(
                    rank, "\u200B".join(
                        person[0]), int(
                        person[2])))

        # We only want to print up to 5 people
        if rank == 5:
            break


# Random Money Spawner
# Every 90 minutes:
#   • check if random money is spawned already
#   • randomly spawn money if there isn't any
@plugin.interval(5400)
def casino_random_money(bot):
    # Check if there's random money spawned
    amount = bot.db.get_channel_value(GCHAN, "random_money", 0)

    # If there's no random_money...
    if not amount:
        # ...generate a number 0-10
        roll = secrets.randbelow(11)
        # chose 6 just because
        if roll == 6:
            # set how much money a user can claim ($10-$100)
            amount = random.randint(10, 100)
            # set random_money in the db
            bot.db.set_channel_value(GCHAN, "random_money", amount)
            # See something, say something!
            # TODO: add some randomness to the message to
            #       prevent notifications and botting.
            return bot.say("${} appeared on the ground.".format(amount), GCHAN)
        else:
            return
    # If the money has been picked...
    elif 10 <= amount <= 100:
        return  # nothing to do
    else:
        return bot.say(
            "xnaas: Error in casino_random_money(). Good luck!",
            GCHAN)


@plugin.command("pick")
@plugin.require_chanmsg
def pick_random_money(bot, trigger):
    """Pick up some money the bot has randomly dropped on the ground."""
    # We're not using gambling_checks() because it's
    # tuned for most other commands in this plugin.
    if trigger.sender == GCHAN:
        pass
    else:
        return bot.reply("This command can only be used in {}".format(GCHAN))

    target = trigger.nick

    check_for_money = bot.db.get_nick_value(target, "currency_amount")
    if check_for_money is None:
        return bot.reply(
            "You can't do this yet! Please run the `.iwantmoney` command.")

    amount = bot.db.get_channel_value(GCHAN, "random_money", 0)

    if not amount:
        insults = [
            "There's no money to pick up, greedy fuck.",
            "Sorry you're poor, but there's no money for you."
        ]
        return bot.reply(secrets.choice(insults))
    elif 10 <= amount <= 100:
        bot.db.set_channel_value(GCHAN, "random_money", 0)
        new_balance = check_for_money + amount
        bot.db.set_nick_value(target, "currency_amount", new_balance)
        balance = "${:,}".format(new_balance)
        bot.reply(
            "Congrats! You picked up ${}. Now you have {}.".format(
                amount, bold(balance)))
    else:
        return bot.say(
            "xnaas: Error in pick_random_money() or casino_random_money(). Good luck!")
