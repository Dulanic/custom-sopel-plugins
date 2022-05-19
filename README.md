# custom-sopel-plugins

These are some [Sopel](https://github.com/sopel-irc/sopel) plugins I've written. While `custom.py` is very, very specific to my chat, the rest are pretty generic and a great addition to any IRC channel.

## [8ball.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/8ball.py)
Just a standard, run-of-the-mill [magic 8-ball](https://en.wikipedia.org/wiki/Magic_8-Ball). Never lies.


## [animals.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/animals.py)
Posts random animal pics from several different APIs.


## [base64coder.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/base64coder.py)
Encode or decode base64 data.


## [casino.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/casino.py)
Allows users to make and gamble away virtual currency.


## [colors.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/colors.py)
Moved from [sopel-color-text](https://github.com/xnaas/sopel-color-text) — don't want to actually deal with publishing to pypi in the future.


## custom.py
Custom commands for [Action Sack](https://actionsack.com)'s Sopel bot. Many of these are highly inappropriate.


## [dadjokes.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/dadjokes.py)
Uses the [icanhazdadjoke API](https://icanhazdadjoke.com/api) to post dad jokes.


## [drg.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/drg.py)
Some custom stuff for [Deep Rock Galactic](https://www.deeprockgalactic.com/).


## [ercot.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/ercot.py)
Pulls basic grid status from [ERCOT](https://www.ercot.com/).


## [hn.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/hn.py)
Gets details from [Hacker News API](https://github.com/HackerNews/API) for HN links.


## [img.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/img.py)
Image searching with [DuckDuckGo Instant Answers API](https://duckduckgo.com/api) and [Google CSE](https://programmablesearchengine.google.com/about/).


## [insult.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/insult.py)
Uses the [Evil Insult Generator](https://evilinsult.com/api/) to insult other users.


## [isbn.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/isbn.py)
Uses the [Open Library Books API](https://openlibrary.org/dev/docs/api/books) to look up a book via ISBN.


## [mcu.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/mcu.py)
Queries the [whenisthenextmcufilm API](https://whenisthenextmcufilm.com) for upcoming MCU movie and show info.


## [nitter.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/nitter.py)
Reads nitter links and sends data to [sopel-twitter](https://github.com/sopel-irc/sopel-twitter/)
for pretty output.


## [nsfw.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/nsfw.py)
RNG of NSFW things.


## [osrs.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/osrs.py)
Queries OSRS HiScores for player stats.


## [penis.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/penis.py)
100% accurate penis measuring.


## [random-apis.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/random-apis.py)
Adds some random APIs for fun.


## [rep.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/rep.py)
Users can increase or decrease each others' reputation.


## [smite_vgs.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/smite_vgs.py)
Adds [Smite's VGS](https://smite.gamepedia.com/Voice_Guided_System) to Sopel.


## [soplex.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/soplex.py)
Uses [PlexAPI](https://github.com/pkkid/python-plexapi) to interface your Sopel bot with your Plex server.


## [steam.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/steam.py)
Uses the [Steam Web API](https://developer.valvesoftware.com/wiki/Steam_Web_API) and some jank
to get Steam store links and player counts.


## [thesaurus.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/thesaurus.py)
Uses [Merriam-Webster's Collegiate Thesaurus API](https://www.dictionaryapi.com/products/api-collegiate-thesaurus) to query synonyms and antonyms.


## [whois.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/whois.py)
Check domain availability. Uses [WhoisXML API](https://www.whoisxmlapi.com).


## [yourmom.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/yourmom.py)
Posts a random joke from [yourmom.txt](https://github.com/xnaas/custom-sopel-plugins/blob/main/yourmom.txt).


## [y'all.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/y'all.py)
Stop spelling y'all wrong.


## [yf.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/yf.py)
Uses the unofficial Yahoo Finance API for things.


## [ytdl.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/ytdl.py)
Uses [youtube-dl](https://youtube-dl.org/) to download and share a video. Would require editing to be useful to anyone else.

---

### Deprecated Plugins

These plugins are deprecated and no longer used or updated.

#### [commodities.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/deprecated/commodities.py)
This was abandoned because Yahoo Finance can do this and more much better and with no limits.

Use [yf.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/yf.py) instead.

Used the [Commodities API](https://commodities-api.com) to get the Brent Crude Oil price ber barrel.

#### [imgur.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/deprecated/imgur.py)
This was abandoned because the Imgur API isn't great for this purpose.

Use [img.py](https://github.com/xnaas/custom-sopel-plugins/blob/main/img.py) instead.

Used the [Imgur API](https://apidocs.imgur.com/) to post image results to chat.
