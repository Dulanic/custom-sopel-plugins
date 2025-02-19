"""
Original author: xnaas (2022)
License: The Unlicense (public domain)
"""
import re
import requests
from sopel import config, plugin
from sopel.config.types import StaticSection, ValidatedAttribute


class WhoisSection(StaticSection):
    api_key = ValidatedAttribute("api_key", str)


def setup(bot):
    bot.config.define_section("whois", WhoisSection)


def configure(config):
    config.define_section("whois", WhoisSection)
    config.whois.configure_setting("api_key", "whoisxmlapi api key")


# this is not 100% foolproof, but it catches a lot
VALID_SLD = "^((?=[a-z0-9-]{1,63})(xn--)?[a-z0-9]+(-[a-z0-9]+)*)+$"


@plugin.commands("whois")
@plugin.example(".whois actionsack.com")
def domain_reg_check(bot, trigger):
    """Check if a domain is registered.
    Doesn't work on stuff like .co.uk or .com.au"""
    domain = trigger.group(3)

    if not domain:
        return bot.reply("I need a domain to check.")

    # credit check
    if domain == "credits":
        url = "https://user.whoisxmlapi.com/user-service/account-balance"
        params = {
            "productId": 1,
            "apiKey": bot.config.whois.api_key
        }
        try:
            credits = requests.get(url, params=params).json()["data"][0]["credits"]
            return bot.say(f"[WHOIS] {credits} credits remaining.")
        except requests.exceptions.RequestException:
            return bot.reply("Issue with API.")

    # normal text → punycode
    # catches some invalid domain stuff
    try:
        domain = domain.encode('idna').decode('ascii')
    except UnicodeError:
        return bot.reply("I need a valid domain to check.")

    # get SLD and TLD for validation checks
    try:
        host = domain.lower().split(".", 1)
        sld = host[0]  # second-level domain
        tld = host[1]  # top-level domain
    except IndexError:
        return bot.reply("I need a valid domain to check.")

    # filter out most invalid SLDs
    if re.search(VALID_SLD, sld):
        pass
    else:
        return bot.reply("I need a valid domain to check.")

    # set valid TLD list from core tld.py
    TLD_LIST = bot.memory["tld_list_cache"]

    # if TLD in invalid, stop now
    if tld not in TLD_LIST:
        return bot.reply("I need a valid domain to check.")

    # re-combine punycode SLD and TLD for API call
    domain = f"{sld}.{tld}"

    # punycode → normal text
    # catches remaining invalid domain stuff
    try:
        sld = sld.encode('ascii').decode('idna')
        tld = tld.encode('ascii').decode('idna')
    except UnicodeError:
        return bot.reply("I need a valid domain to check.")

    try:
        url = "https://domain-availability.whoisxmlapi.com/api/v1"
        params = {
            "apiKey": bot.config.whois.api_key,
            "domainName": domain,
            "mode": "DNS_AND_WHOIS",
            "credits": "WHOIS"
        }
        result = requests.get(url, params=params).json()

        # re-combine normal text SLD and TLD for pretty output
        domain = f"{sld}.{tld}"

        # Print domain availability
        if "DomainInfo" in result:
            domain_avail = result["DomainInfo"]["domainAvailability"]
            return bot.say(f"{domain} is {domain_avail}.")
        # Error Handling from API
        elif "ErrorMessage" in result:
            error_message = result["ErrorMessage"]["msg"]
            return bot.say(f"{domain}: {error_message}")
        else:
            return bot.reply("Issue with API.")
    except requests.exceptions.RequestException:
        return bot.reply("Issue with API.")
