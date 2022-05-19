from sopel import plugin, tools
from sopel.formatting import bold, color, colors, plain


@plugin.output_prefix('[REP] ')
@plugin.rate(user=60)
@plugin.require_account('You must have a registered account to participate.', True)
@plugin.require_chanmsg
@plugin.rule(r'^(?P<target>[^\s,*?.!@:<>\'\";#/]{1,32})(?P<PoM>[+-]{2})$')
def rep(bot, trigger):
    target = plain(trigger.group('target') or '')
    if not target:
        return plugin.NOLIMIT
    target = tools.Identifier(target)
    if target not in bot.channels[trigger.sender].users:
        return plugin.NOLIMIT
    if not bot.channels[trigger.sender].users[target].account:
        bot.say(f"{target} is not registered and can't earn reputation.")
        return plugin.NOLIMIT

    current_rep = bot.db.get_nick_value(target, 'rep', 0)

    PoM = trigger.group('PoM')  # Plus or Minus
    if PoM == '++':
        if target == trigger.nick:
            bot.reply('Trying to rep++ yourself is beyond pathetic...')
            bot.action('looks away in disgust.')
            return
        new_rep = current_rep + 1
    elif PoM == '--':
        new_rep = current_rep - 1
    else:
        return plugin.NOLIMIT

    bot.db.set_nick_value(target, 'rep', new_rep)
    new_rep = bold(f'{new_rep:,}')
    bot.say(f'{target}: {current_rep:,} → {new_rep}')


@plugin.command('rep')
@plugin.output_prefix('[REP] ')
@plugin.rate(user=3)
@plugin.require_account('You must have a registered account to participate.', True)
@plugin.require_chanmsg
def rep_check(bot, trigger):
    target = plain(trigger.group(3) or trigger.nick)
    target = tools.Identifier(target)
    if target not in bot.channels[trigger.sender].users:
        return bot.say(f'{target} is not here.')

    if not bot.channels[trigger.sender].users[target].account:
        bot.say(f"{target} is not registered and can't earn reputation.")
        return plugin.NOLIMIT

    rep = bot.db.get_nick_value(target, 'rep', 0)
    if rep > 0:
        rep = bold(color(f'{rep:,}', colors.GREEN))
    elif rep < 0:
        rep = bold(color(f'{rep:,}', colors.RED))
    else:
        rep = color(f'{rep:,}', colors.GREY)
    bot.say(f'{target}: {rep}')


@plugin.command('reptop', 'replow')
@plugin.output_prefix('[REP] ')
@plugin.rate(user=5)
@plugin.require_account('You must have a registered account to participate.', True)
def rep_list(bot, trigger):
    cmd = trigger.group(1).lower()
    query =  "SELECT canonical, key, value FROM nick_values a join nicknames "
    query += "b on a.nick_id = b.nick_id WHERE key='rep' "
    if cmd == 'reptop':
        query += "ORDER BY cast(value as int) DESC;"
    elif cmd == 'replow':
        query += "ORDER BY cast(value as int) ASC;"
    else:
        return plugin.NOLIMIT

    lb = bot.db.execute(query).fetchall()
    if not lb:
        return bot.say('Nobody has any reputation yet!')

    rep_list = []
    for index, person in enumerate(lb):
        name = '\u200B'.join(person[0])
        rep = int(person[2])
        if cmd == 'reptop' and rep < 0:
            pass
        elif cmd == 'replow' and rep >= 0:
            pass
        else:
            if rep > 0:
                rep = bold(color(f'{rep:,}', colors.GREEN))
            elif rep < 0:
                rep = bold(color(f'{rep:,}', colors.RED))
            else:
                rep = color(f'{rep:,}', colors.GREY)
            rep_list.append(f'{name}: {rep}')
        # we only want to print up to 5 people
        if index == 5:
            break

    if cmd == 'reptop' and not rep_list:
        return bot.say('No one with positive reputation...')
    if cmd == 'replow' and not rep_list:
        return bot.say('No one with negative reputation!')

    bot.say(', '.join(rep_list))


@plugin.command('repset')
@plugin.output_prefix('[REP ADMIN] ')
@plugin.require_admin
@plugin.require_chanmsg
def rep_set(bot, trigger):
    target = plain(trigger.group(3) or '')
    if not target:
        return bot.say('I need a target...')
    target = tools.Identifier(target)
    if target not in bot.channels[trigger.sender].users:
        return bot.say(f'{target} is not here.')
    if not bot.channels[trigger.sender].users[target].account:
        bot.say(f"{target} is not registered and can't earn reputation.")
        return plugin.NOLIMIT

    try:
        new_rep = int(plain(trigger.group(4)))
    except ValueError:
        return bot.say(f'{new_rep} is not an integer.')

    current_rep = bot.db.get_nick_value(target, 'rep', 0)
    bot.db.set_nick_value(target, 'rep', new_rep)
    new_rep = bold(f'{new_rep:,}')
    bot.say(f'{target}: {current_rep:,} → {new_rep}')


@plugin.command('repwipe')
@plugin.output_prefix('[REP ADMIN] ')
@plugin.require_admin
def rep_wipe(bot, trigger):
    target = plain(trigger.group(3) or '')
    if not target:
        return bot.say('I need a target...')
    target = tools.Identifier(target)
    bot.db.delete_nick_value(target, 'rep')
    bot.say(f'reputation data wiped for: {bold(target)}')
