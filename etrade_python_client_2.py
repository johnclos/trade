"""This Python script provides examples on using the E*TRADE API endpoints"""
# From:  https://developer.etrade.com/support/downloads
from __future__ import print_function
import webbrowser
import json
import logging
import configparser
import sys
import requests
from rauth import OAuth1Service
from logging.handlers import RotatingFileHandler
from accounts.accounts import Accounts
from market.market import Market
from options.options import Options
from urllib.parse import urlencode

# loading configuration file
config = configparser.ConfigParser()

# config.read('C:/Users/jjel0/OneDrive/Data_Analytics/repositories/config_sandbox.ini')
config.read('C:/Users/jjel0/OneDrive/Data_Analytics/repositories/config_live.ini')

# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("python_client.log", maxBytes=5*1024*1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)

def oauth():
    """Allows user authorization for the sample application with OAuth 1"""
    etrade = OAuth1Service(
        name = "etrade",
        consumer_key = config["DEFAULT"]["CONSUMER_KEY"],
        consumer_secret = config["DEFAULT"]["CONSUMER_SECRET"],
        request_token_url = "https://api.etrade.com/oauth/request_token",
        access_token_url = "https://api.etrade.com/oauth/access_token",
        authorize_url = "https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        base_url = "https://api.etrade.com")
    
    menu_items = {"1": "Sandbox Consumer Key",
                  "2": "Live Consumer Key",
                  "3": "Exit"}
    while True:
        print("")
        options = menu_items.keys()
        for entry in options:
            print(entry + ")\t" + menu_items[entry])
        selection = input("Please select Consumer Key Type: ")
        if selection == "1":
            base_url = config["DEFAULT"]["SANDBOX_BASE_URL"]
            break
        elif selection == "2":
            base_url = config["DEFAULT"]["PROD_BASE_URL"]
            break
        elif selection == "3":
            break
        else:
            print("Unknown Option Selected!")
    print("")

    # Step 1: Get OAuth 1 request token and secret 
    request_token, request_token_secret = etrade.get_request_token(
        params = {"oauth_callback": "oob", "format": "json", "range": "1y", "interval": "day"})

    # Step 2: Go through the authentication flow. Login to E*TRADE.
    # After you login, the page will provide a verification code to enter.
    authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
    webbrowser.open(authorize_url)
    text_code = input("Please accept agreement and enter verification code from browser: ")

    # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
    session = etrade.get_auth_session(request_token,
                                  request_token_secret,
                                  params={"oauth_verifier": text_code})

    main_menu(session, base_url)


def main_menu(session, base_url):
    """
    Provides the different options for the sample application: Market Quotes, Account List, Historical Data

    :param session: authenticated session
    """

    menu_items = {
        "1": "Market Quotes",
        "2": "Account List",
        "3": "Options Chain",
        "4": "Options Expire Dates",
        "5": "Historical Market Data",  # New option
        "6": "Exit"
    }

    while True:
        print("")
        options = menu_items.keys()
        for entry in options:
            print(entry + ")\t" + menu_items[entry])
        selection = input("Please select an option: ")
        if selection == "1":
            market = Market(session, base_url)
            market.quotes()
        elif selection == "2":
            accounts = Accounts(session, base_url)
            accounts.account_list()
        elif selection == "3":
            options = Options(session, base_url)
            options.OptionsQuotes()
        elif selection == "4":
            options = Options(session, base_url)
            options.OptionsExpDate()
        elif selection == "5":  # New option for historical data
            market = Market(session, base_url)
            get_historical_data(market)
        elif selection == "6":
            break
        else:
            print("Unknown Option Selected!")

def get_historical_data(self, symbol, range, interval):
    """
    Fetch historical market data.

    :param symbol: Stock symbol
    :param range: Time range for data (e.g., 1d, 5d, 1y)
    :param interval: Interval between data points (e.g., day, hour)
    :return: Response JSON or None
    """
    url = f"{self.base_url}/v1/market/quote/{symbol}"  # Confirm this endpoint supports historical data
    url = f"https://apisb.etrade.com/v1/market/quote/AAPL?range=1y&interval=day"  # Confirm this endpoint supports historical data
    params = {"range": range, "interval": interval}
    response = self.session.get(url, params=params)

    print(f"Request URL: {response.url}")  # Log the full request URL
    print(f"Response Status Code: {response.status_code}")  # Log the response status

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            print(f"Response Content: {response.text}")
            return None
    else:
        print(f"Error fetching historical data: {response.status_code} - {response.text}")
        return None


if __name__ == "__main__":
    oauth()
