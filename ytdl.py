from sopel import plugin
from sopel.formatting import bold, italic
from sopel.tools import SopelIdentifierMemory
import re
import yt_dlp as youtube_dl


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
@plugin.search(
    r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})")
@plugin.unblockable
def youtube_link_log(bot, trigger):
    video_id = trigger.group(6)

    if not video_id:
        bot.say("xnaas: YouTube link logging error...good luck!")
        return

    # Logs latest YouTube link per channel
    bot.memory["youtube_ids"][trigger.sender] = video_id

    # Debugging in Prod
    # bot.say("Message logged. ID logged: {}".format(bold(video_id)))


# Tells us what ID is logged for this channel.
@plugin.command("ytid")
def temp_youtube_id(bot, trigger):
    try:
        bot.reply("The currently stored ID for this channel is {}.".format(
            bold(bot.memory["youtube_ids"][trigger.sender])))
    except KeyError:
        bot.reply("I have no IDs stored for this channel.")


# Download MP4-compatible formats for MP4 container
ytdl_opts = {
    "format": "bestvideo[height<=?1080]+bestaudio/best",
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
        with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
            meta = ytdl.extract_info(url, download=False)
            id = meta["id"]
            ext = meta["ext"]
            dur = meta["duration"]
            if not dur:
                bot.reply(
                    "This video has no duration (livestream?) and cannot be downloaded.")
                return
            if dur > 600:
                bot.reply(
                    "This video is longer than 10 minutes and cannot be download, sorry!")
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
                "This video has no duration (livestream?) and cannot be downloaded.")
            return
