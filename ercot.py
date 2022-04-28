"""
Original author: xnaas
License: The Unlicense (public domain)
"""
from sopel import plugin
import requests


@plugin.commands("ercot")
@plugin.output_prefix("[ERCOT] ")
def ercot_status(bot, trigger):
    base_url = "https://www.ercot.com/api/1/services/read/dashboards"
    try:
        # Status
        url_status = f"{base_url}/daily-prc.json"
        result = requests.get(url_status).json()["current_condition"]
        status = result["title"]
        op_res = result["prc_value"]
        # Frequency
        url_freq = f"{base_url}/ancillaryServices.json"
        freq = requests.get(url_freq).json()["data"][0]["currentFrequency"]
    except Exception as e:
        return bot.reply(e)

    bot.say(f"Status: {status} ({freq}Hz) | Reserves: {op_res}MWh")
