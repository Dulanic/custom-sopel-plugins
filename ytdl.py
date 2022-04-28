"""
Original author: xnaas
License: The Unlicense (public domain)
"""
from sopel import plugin
from sopel.formatting import bold, italic
from sopel.tools import SopelIdentifierMemory
import re
import yt_dlp as youtube_dl


# Should match all valid YouTube links.
VALID_YT_LINK = r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"


# YouTube Link Logger
def setup(bot):
    if "youtube_ids" not in bot.memory:
        bot.memory["youtube_ids"] = SopelIdentifierMemory()


# YouTube Link Logger
def shutdown(bot):
    try:
        del bot.memory["youtube_ids"]
    except KeyError:
        pass


# YouTube Link Logger
@plugin.echo
@plugin.priority("low")
@plugin.require_chanmsg
@plugin.search(VALID_YT_LINK)
@plugin.unblockable
def youtube_link_log(bot, trigger):
    video_id = trigger.group(6)

    if not video_id:
        bot.say("xnaas: YouTube link logging error...good luck!")
        return

    # Logs latest YouTube link per channel
    bot.memory["youtube_ids"][trigger.sender] = video_id


# Tells us what ID is logged for this channel.
@plugin.command("ytid")
@plugin.require_chanmsg
def temp_youtube_id(bot, trigger):
    try:
        bot.reply("The currently stored ID for this channel is {}.".format(
            bold(bot.memory["youtube_ids"][trigger.sender])))
    except KeyError:
        bot.reply("I have no ID stored for this channel.")


# Download MP4-compatible formats for MP4 container
ytdl_opts = {
    "format": "bestvideo[height<=?1080]+bestaudio/best",
    "format_sort": ["+codec:avc:m4a"],  # prioritize h264 and m4a
    "merge_output_format": "mp4",
    "noplaylist": True,
    "forcejson": True,
    "outtmpl": "/mnt/media/websites/actionsack.com/tmp/%(id)s.%(ext)s"
}


@plugin.command("ytdl")
@plugin.output_prefix("[youtube-dl] ")
@plugin.rate(user=600)
def ytdl(bot, trigger):
    """Uses yt-dlp to download a video and post it to chat."""
    url = trigger.group(3)

    if not url:
        try:
            url = bot.memory["youtube_ids"][trigger.sender]
        except KeyError:
            bot.reply("You've given me nothing to work with...what the Hell do you want?!")
            return plugin.NOLIMIT

    try:
        with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
            bot.say(italic("Processing..."))
            meta = ytdl.extract_info(url, download=False)
            id = meta["id"]
            ext = meta["ext"]
            dur = meta["duration"]
            if not dur:
                bot.reply("This video has no duration (livestream?) and won't be downloaded.")
                return plugin.NOLIMIT
            if dur > 480:
                bot.reply("This video is longer than 8 minutes and won't be downloaded.")
                return plugin.NOLIMIT
            else:
                bot.say(italic("Downloading..."))
                ytdl.download([url])
                return bot.say(f"https://actionsack.com/tmp/{id}.{ext}")
    except youtube_dl.utils.DownloadError:
        bot.reply("Download error or invalid link. Please try again.")
        return plugin.NOLIMIT
    except KeyError:
        if any((re.search(r"v\.redd\.it\/", url),
                re.search(r"video\.twimg\.com\/", url),
                re.search(r"cdn\.discordapp\.com\/", url),
                re.search(r"vm\.tiktok\.com\/", url))):
            bot.say(italic("Downloading..."))
            ytdl.download([url])
            return bot.say(f"https://actionsack.com/tmp/{id}.{ext}")
        else:
            bot.reply("This video has no duration (livestream?) and won't be downloaded.")
            return plugin.NOLIMIT


# Download mp4/audio (m4a)
ytdla_opts = {
    "format": "bestaudio/best",
    "format_sort": ["+codec:avc:m4a"],  # prioritize m4a
    "merge_output_format": "m4a",
    "final_ext": "m4a",
    "noplaylist": True,
    "forcejson": True,
    "outtmpl": "/mnt/media/websites/actionsack.com/tmp/%(id)s.%(ext)s",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "m4a"
    }]
}


@plugin.command("ytdla")
@plugin.output_prefix("[youtube-dl] ")
def ytdla(bot, trigger):
    """Uses yt-dlp to download audio from a YouTube video and post it to chat."""
    url = trigger.group(3)
    from_id = False

    # If no url, check memory for a stored YouTube ID
    if not url:
        try:
            url = bot.memory["youtube_ids"][trigger.sender]
            from_id = True
        except KeyError:
            return bot.reply("You've given me nothing to work with...what the Hell do you want?!")

    # Check if "url" is a valid YouTube ID
    if re.search(r"^[^&=%\?]{11}$", url):
        from_id = True

    if re.search(VALID_YT_LINK, url) or from_id:
        pass
    else:
        return bot.reply("YouTube links or IDs only.")

    try:
        with youtube_dl.YoutubeDL(ytdla_opts) as ytdl:
            bot.say(italic("Processing..."))
            meta = ytdl.extract_info(url, download=False)
            id = meta["id"]
            ext = meta["audio_ext"]
            dur = meta["duration"]
            if not dur:
                return bot.reply("This video has no duration (livestream?) and won't be downloaded.")
            if dur > 900:
                return bot.reply("This video is longer than 15 minutes and won't be downloaded.")
            else:
                bot.say(italic("Downloading..."))
                ytdl.download([url])
                return bot.say(f"https://actionsack.com/tmp/{id}.{ext}")
    except youtube_dl.utils.DownloadError:
        return bot.reply("Download error or invalid link. Please try again.")
    except KeyError:
        return bot.reply("This video has no duration (livestream?) and won't be downloaded.")
