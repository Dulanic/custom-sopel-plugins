from sopel import plugin
import requests


@plugin.commands("ercot")
@plugin.output_prefix("[ERCOT] ")
def ercot_status(bot, trigger):
    base_url = "https://www.ercot.com/api/1/services/read/dashboards"
    try:
        # Status
        url_status = "{}/daily-prc.json".format(base_url)
        result = requests.get(url_status).json()["current_condition"]
        status = result["title"]
        op_res = result["prc_value"]

        # Frequency
        url_freq = "{}/ancillaryServices.json".format(base_url)
        freq = requests.get(url_freq).json()["data"][0]["currentFrequency"]
    except Exception as e:
        return bot.reply(e)

    bot.say("Status: {} ({}Hz) | Reserves: {}MWh".format(status, freq, op_res))
