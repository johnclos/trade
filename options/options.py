import json
import logging
from logging.handlers import RotatingFileHandler
import configparser
import pandas as pd

# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("python_client.log", maxBytes=5 * 1024 * 1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)

# loading configuration file
config = configparser.ConfigParser()
# config.read('C:/Users/jjel0/OneDrive/Data_Analytics/repositories/config_sandbox.ini')
config.read('C:/Users/jjel0/OneDrive/Data_Analytics/repositories/config_live.ini')

# E*TRADE:
# (01/10/2024 11:12 AM) (Ref No.: 10497301)
# Dear Mr. Clos,

# This message is regarding your API inquiry.

# Note that we are using rauth python library and you have to add your query parameters in params in the below way.

# I am giving an example below for https://api.etrade.com/v1/market/optionchains?symbol=GOOG. Please change url and parameters 
    # based on the api you are trying to call.

# CODE:
# loading configuration file
# config = configparser.ConfigParser()
# config.read('config.ini')
# url = self.base_url + "/v1/market/optionchains.json"

# params ={"symbol": "AAPL"}
# headers ={"consumerkey": config["DEFAULT"]["CONSUMER_KEY"]}

# response = self.session.get(url, header_auth=True, params=params, headers=headers)

# Sincerely,
# Christopher Gittens
# 9 a.m. ET - 5:45 p.m. ET, Monday - Friday
# 1-800-ETRADE-1 (800-387-2331)
# Financial Service Representative 3
# E*TRADE Securities LLC
# Morgan Stanley Smith Barney LLC


class Options:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def OptionsQuotes(self):
        """
        Calls quotes API to provide quote details for equities, options, and mutual funds

        :param self: Passes authenticated session in parameter
        """
        symbols = input("\nPlease enter Stock Symbol: ")

        # loading configuration file
        config = configparser.ConfigParser()
        # config.read('C:/Users/jjel0/OneDrive/Data_Analytics/repositories/config_sandbox.ini')
        config.read('C:/Users/jjel0/OneDrive/Data_Analytics/repositories/config_live.ini')
              
        url = self.base_url + "/v1/market/optionchains.json"

        params ={"symbol": symbols}
        headers ={"consumerkey": config["DEFAULT"]["CONSUMER_KEY"]}

        response = self.session.get(url, header_auth=True, params=params, headers=headers)

        # Make API call for GET request
        logger.debug("Request Header: %s", response.request.headers)
        print("Request Header: %s", response.request.headers)

        if response is not None and response.status_code == 200:

            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
            print("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
            
            # put in json format and save to a json file
            response_json = json.dumps(parsed, indent=4, sort_keys=True)
            print(response_json)
            f = open("C:/Users/jjel0/OneDrive/Data_Analytics/repositories/trade/response_json.json", "w")
            f.write(response_json)
            f.close()

            # Handle and parse response
            print("")
            data = response.json()
            if data is not None and "QuoteResponse" in data and "QuoteData" in data["QuoteResponse"]:
                for quote in data["QuoteResponse"]["QuoteData"]:
                    if quote is not None and "dateTime" in quote:
                        print("Date Time: " + quote["dateTime"])
                    if quote is not None and "Product" in quote and "symbol" in quote["Product"]:
                        print("Symbol: " + quote["Product"]["symbol"])
                    if quote is not None and "Product" in quote and "securityType" in quote["Product"]:
                        print("Security Type: " + quote["Product"]["securityType"])
                    if quote is not None and "All" in quote and "lastTrade" in quote["All"]:
                        print("Last Price: " + str(quote["All"]["lastTrade"]))
                    if quote is not None and "All" in quote and "changeClose" in quote["All"] \
                        and "changeClosePercentage" in quote["All"]:
                        print("Today's Change: " + str('{:,.3f}'.format(quote["All"]["changeClose"])) + " (" +
                              str(quote["All"]["changeClosePercentage"]) + "%)")
                    if quote is not None and "All" in quote and "lastTrade" in quote["All"]:
                        print("Open: " + str('{:,.2f}'.format(quote["All"]["lastTrade"])))
                    if quote is not None and "All" in quote and "previousClose" in quote["All"]:
                        print("Previous Close: " + str('{:,.2f}'.format(quote["All"]["previousClose"])))
                    if quote is not None and "All" in quote and "bid" in quote["All"] and "bidSize" in quote["All"]:
                        print("Bid (Size): " + str('{:,.2f}'.format(quote["All"]["bid"])) + "x" + str(
                            quote["All"]["bidSize"]))
                    if quote is not None and "All" in quote and "ask" in quote["All"] and "askSize" in quote["All"]:
                        print("Ask (Size): " + str('{:,.2f}'.format(quote["All"]["ask"])) + "x" + str(
                            quote["All"]["askSize"]))
                    if quote is not None and "All" in quote and "low" in quote["All"] and "high" in quote["All"]:
                        print("Day's Range: " + str(quote["All"]["low"]) + "-" + str(quote["All"]["high"]))
                    if quote is not None and "All" in quote and "totalVolume" in quote["All"]:
                        print("Volume: " + str('{:,}'.format(quote["All"]["totalVolume"])))
            else:
                # Handle errors
                if data is not None and 'QuoteResponse' in data and 'Messages' in data["QuoteResponse"] \
                        and 'Message' in data["QuoteResponse"]["Messages"] \
                        and data["QuoteResponse"]["Messages"]["Message"] is not None:
                    for error_message in data["QuoteResponse"]["Messages"]["Message"]:
                        print("Error: " + error_message["description"])
                else:
                    print("Error: Quote API service error")
        
        else:
            logger.debug("Response Body: %s", response)
            print("Response Body: %s", response)
            print("Error: Quote API service error")
    
    
    def OptionsExpDate(self):
        """
        Calls quotes API to provide quote details for equities, options, and mutual funds

        :param self: Passes authenticated session in parameter
        """
        symbols = input("\nPlease enter Stock Symbol: ")

        # loading configuration file
        config = configparser.ConfigParser()
        # config.read('C:/Users/jjel0/OneDrive/Data_Analytics/repositories/config_sandbox.ini')
        config.read('C:/Users/jjel0/OneDrive/Data_Analytics/repositories/config_live.ini')
        # url = "https://api.etrade.com/v1/market/optionexpiredate?symbol=GOOG&amp;expiryType=ALL.json"    
        # url = self.base_url + "v1/market/optionexpiredate?symbol=" + symbols + "&amp;expiryType=ALL.json"
        url = self.base_url + "/v1/market/optionexpiredate.json"

        params ={"symbol": symbols}
        headers ={"consumerkey": config["DEFAULT"]["CONSUMER_KEY"]}

        response = self.session.get(url, header_auth=True, params=params, headers=headers)
        print(response)
        # Make API call for GET request
        logger.debug("Request Header: %s", response.request.headers)
        # print("Request Header: %s", response.request.headers)

        if response is not None and response.status_code == 200:

            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
            print("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
            response_exp_json = json.dumps(parsed, indent=4, sort_keys=True)
            print(response_exp_json)
            f = open("C:/Users/jjel0/OneDrive/Data_Analytics/repositories/trade/response_exp_json.json", "w")
            f.write(response_exp_json)
            f.close()
            # Handle and parse response
            # print("")
            # data = response.json()
            # if data is not None and "QuoteResponse" in data and "QuoteData" in data["QuoteResponse"]:
            #     for quote in data["QuoteResponse"]["QuoteData"]:
            #         if quote is not None and "dateTime" in quote:
            #             # print("Date Time: " + quote["dateTime"])
            #         if quote is not None and "Product" in quote and "symbol" in quote["Product"]:
            #             # print("Symbol: " + quote["Product"]["symbol"])
            #         if quote is not None and "Product" in quote and "securityType" in quote["Product"]:
            #             # print("Security Type: " + quote["Product"]["securityType"])
            #         if quote is not None and "All" in quote and "lastTrade" in quote["All"]:
            #             # print("Last Price: " + str(quote["All"]["lastTrade"]))
            #         if quote is not None and "All" in quote and "changeClose" in quote["All"] \
            #             and "changeClosePercentage" in quote["All"]:
            #             # print("Today's Change: " + str('{:,.3f}'.format(quote["All"]["changeClose"])) + " (" +
            #                 #   str(quote["All"]["changeClosePercentage"]) + "%)")
            #         if quote is not None and "All" in quote and "lastTrade" in quote["All"]:
            #             # print("Open: " + str('{:,.2f}'.format(quote["All"]["lastTrade"])))
            #         if quote is not None and "All" in quote and "previousClose" in quote["All"]:
            #             # print("Previous Close: " + str('{:,.2f}'.format(quote["All"]["previousClose"])))
            #         if quote is not None and "All" in quote and "bid" in quote["All"] and "bidSize" in quote["All"]:
            #             # print("Bid (Size): " + str('{:,.2f}'.format(quote["All"]["bid"])) + "x" + str(
            #                 # quote["All"]["bidSize"]))
            #         if quote is not None and "All" in quote and "ask" in quote["All"] and "askSize" in quote["All"]:
            #             # print("Ask (Size): " + str('{:,.2f}'.format(quote["All"]["ask"])) + "x" + str(
            #                 # quote["All"]["askSize"]))
            #         if quote is not None and "All" in quote and "low" in quote["All"] and "high" in quote["All"]:
            #             # print("Day's Range: " + str(quote["All"]["low"]) + "-" + str(quote["All"]["high"]))
            #         if quote is not None and "All" in quote and "totalVolume" in quote["All"]:
            #             # print("Volume: " + str('{:,}'.format(quote["All"]["totalVolume"])))
            # else:
            #     # Handle errors
            #     if data is not None and 'QuoteResponse' in data and 'Messages' in data["QuoteResponse"] \
            #             and 'Message' in data["QuoteResponse"]["Messages"] \
            #             and data["QuoteResponse"]["Messages"]["Message"] is not None:
            #         for error_message in data["QuoteResponse"]["Messages"]["Message"]:
            #             # print("Error: " + error_message["description"])
            #     else:
            #         # print("Error: Quote API service error")
        
        else:
            logger.debug("Response Body: %s", response)
            # print("Response Body: %s", response)
            # print("Error: Quote API service error")
        
