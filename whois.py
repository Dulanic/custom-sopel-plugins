"""
This is a huge WIP. Needs a lot of work, still.
"""

from sopel import config, plugin
from sopel.config.types import StaticSection, ValidatedAttribute
import re
import requests


class WhoisSection(StaticSection):
    api_key = ValidatedAttribute("api_key", str)


def setup(bot):
    bot.config.define_section("whois", WhoisSection)


def configure(config):
    config.define_section("whois", WhoisSection)
    config.whois.configure_setting("api_key", "whoisxmlapi api key")


# TODO: https://data.iana.org/TLD/tlds-alpha-by-domain.txt
VALID_DOMAIN = r"^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$"


@plugin.commands("whois")
@plugin.example(".whois actionsack.com")
def domain_reg_check(bot, trigger):
    """Check if a domain is registered."""
    domain = trigger.group(3)

    if not domain:
        return bot.reply("I need a domain, idiot.")

    # convert to punycode if needed
    domain = domain.encode('idna').decode('ascii')

    if re.search(VALID_DOMAIN, domain):
        try:
            url = "https://domain-availability.whoisxmlapi.com/api/v1"
            params = {
                "apiKey": bot.config.whois.api_key,
                "domainName": domain,
                "mode": "DNS_AND_WHOIS",
                "credits": "DA"
            }
            result = requests.get(url, params=params).json()

            # Error Handling from API
            if "ErrorMessage" in result:
                error_message = result["ErrorMessage"]["msg"]
                domain = domain.encode('ascii').decode('idna')
                return bot.say("{}: {}".format(domain, error_message))
            # Print domain availability
            elif "DomainInfo" in result:
                domain_avail = result["DomainInfo"]["domainAvailability"]
                # domain = result["DomainInfo"]["domainName"]
                domain = domain.encode('ascii').decode('idna')
                return bot.say("{} is {}.".format(domain, domain_avail))
            else:
                return bot.reply("Issue with API.")

        except Exception as e:
            return bot.reply(e)
    else:
        return bot.reply("I need a valid domain, el stupido.")
