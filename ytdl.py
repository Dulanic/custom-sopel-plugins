from __future__ import absolute_import, division, print_function, unicode_literals
from sopel import module, tools
import os
import youtube_dl


ydl_opts = {
    "format": "bestvideo[height<=?1080]+bestaudio/best",
    "merge_output_format": "mp4",
    "noplaylist": True,
    "forcejson": True,
    "outtmpl": "/mnt/media/websites/actionsack.com/tmp/%(id)s.%(ext)s"
}


@module.commands("ytdl")
def ytdl(bot, trigger):
    """Uses youtube-dl to download a video and post it to chat."""
    url = trigger.group(3)

    if not url:
        bot.reply("I need a link, silly!")
        return
    url = tools.Identifier(url)

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            id = meta["id"]
            ext = meta["ext"]
            ydl.download([url])
            bot.say("https://actionsack.com/tmp/{}.{}".format(id, ext))
    except youtube_dl.utils.DownloadError:
        bot.reply("Please submit a valid link.")
