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
def ytdl(bot, trigger):
    """Uses youtube-dl to download a video and post it to chat."""
    url = trigger.group(3)

    if not url:
        try:
            url = bot.memory["youtube_ids"][trigger.sender]
        except KeyError:
            bot.reply(
                "You've given me nothing to work with...what the Hell do you want?!")
            return

    try:
        # https://github.com/yt-dlp/yt-dlp/issues/2396#issuecomment-1021210484
        if re.search("tiktok", url):
            youtube_dl.utils.std_headers["User-Agent"] = "facebookexternalhit/1.1"

        with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
            bot.say(italic("Processing..."))
            meta = ytdl.extract_info(url, download=False)
            id = meta["id"]
            ext = meta["ext"]
            dur = meta["duration"]
            if not dur:
                bot.reply(
                    "This video has no duration (livestream?) and won't be downloaded.")
                return
            if dur > 600:
                bot.reply(
                    "This video is longer than 10 minutes and won't be downloaded.")
                return
            else:
                bot.say(italic("Downloading..."))
                ytdl.download([url])
                bot.say("https://actionsack.com/tmp/{}.{}".format(id, ext))
                return
    except youtube_dl.utils.DownloadError:
        bot.reply("Please submit a valid link.")
    except KeyError:
        if re.search(r"v\.redd\.it\/", url):
            bot.say(italic("Downloading..."))
            ytdl.download([url])
            bot.say("https://actionsack.com/tmp/{}.{}".format(id, ext))
            return
        if re.search(r"video\.twimg\.com\/", url):
            bot.say(italic("Downloading..."))
            ytdl.download([url])
            bot.say("https://actionsack.com/tmp/{}.{}".format(id, ext))
            return
        if re.search(r"cdn\.discordapp\.com\/", url):
            bot.say(italic("Downloading..."))
            ytdl.download([url])
            bot.say("https://actionsack.com/tmp/{}.{}".format(id, ext))
            return
        if re.search(r"vm\.tiktok\.com\/", url):
            bot.say(italic("Downloading..."))
            ytdl.download([url])
            bot.say("https://actionsack.com/tmp/{}.{}".format(id, ext))
            return
        else:
            bot.reply(
                "This video has no duration (livestream?) and won't be downloaded.")
            return


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
    """Uses youtube-dl to download audio from a video and post it to chat."""
    url = trigger.group(3)
    from_id = False

    # If no url, check memory for a stored YouTube ID
    if not url:
        try:
            url = bot.memory["youtube_ids"][trigger.sender]
            from_id = True
        except KeyError:
            bot.reply(
                "You've given me nothing to work with...what the Hell do you want?!")
            return

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
                bot.reply(
                    "This video has no duration (livestream?) and won't be downloaded.")
                return
            if dur > 600:
                bot.reply(
                    "This video is longer than 10 minutes and won't be downloaded.")
                return
            else:
                bot.say(italic("Downloading..."))
                ytdl.download([url])
                bot.say("https://actionsack.com/tmp/{}.{}".format(id, ext))
                return
    except youtube_dl.utils.DownloadError:
        bot.reply("Please submit a valid link.")
    except KeyError:
        bot.reply(
            "This video has no duration (livestream?) and won't be downloaded.")
        return
