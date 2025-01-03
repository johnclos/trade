import json
import logging
from logging.handlers import RotatingFileHandler

# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("python_client.log", maxBytes=5 * 1024 * 1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)       

class Options:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    
    # Get Option Chains
    # Description
    # This API returns a list of option chains for a specific underlying instrument. The request must specify an 
    #     # instrument, the month the option expires, and whether you are interested in calls, puts, or both. Values 
    #     # returned include the option pair count and information about each option pair, including the type, call count, 
    #     # symbol, product, date, and strike price..

    # HTTP Method: GET
    # Live URL:  https://api.etrade.com/v1/market/optionchains?symbol={symbol}

    # Sandbox URL:  https://apisb.etrade.com/v1/market/optionchains?symbol={symbol}

    def OptionsQuote(self):
        """
        Calls quotes API to provide quote details for equities, options, and mutual funds

        :param self: Passes authenticated session in parameter
        """
        symbols = input("\nPlease enter Stock Symbol: ")

        # URL for the API endpoint
        # url = "https://apisb.etrade.com/v1/market/optionexpiredate?symbol=GOOGL&expiryType=ALL" # self.base_url + "/v1/market/optionchains?symbol=" + symbols # + ".json"
        url = self.base_url + "/v1/market/quote/" + symbols + ".json"
        print(url)
        # Make API call for GET request
        response = self.session.get(url)
        logger.debug("Request Header: %s", response.request.headers)

        if response is not None and response.status_code == 200:

            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))

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
            print("Error: Quote API service error")
    

    # Get Option Expire Dates
    # Description
    # Returns a list of dates suitable for structuring an option table display. The dates are used to group option data 
        # (returned by the optionchains method) for a specified underlier, creating a table display.

    # HTTP Method: GET
    # Live URL:  https://api.etrade.com/v1/market/optionexpiredate?symbol={symbol}
                
    # Sandbox URL:  https://apisb.etrade.com/v1/market/optionexpiredate?symbol={symbol}
    
    def OptionsExpDate(self):
        """
        Calls quotes API to provide quote details for equities, options, and mutual funds

        :param self: Passes authenticated session in parameter
        """
        symbols = input("\nPlease enter Stock Symbol: ")

        # URL for the API endpoint
        # url = self.base_url + "/v1/market/optionexpiredate?symbol=GOOGL&amp;expiryType=ALL"
        url = self.base_url + "/v1/market/quote/" + symbols + ".json"
        # Make API call for GET request
        response = self.session.get(url)
        logger.debug("Request Header: %s", response.request.headers)

        if response is not None and response.status_code == 200:

            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))

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
            print("Error: Quote API service error")



