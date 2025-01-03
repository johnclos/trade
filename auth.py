# From:  https://nexusfission.com/2023/11/14/etrade-api-setup-using-python-automation-oauth-1-0-explained/
import os
from rauth import OAuth1Service
# import const
import constants # as const
consts = constants.Constants()
 
print("A")
class EtradeAuth():
  print("B")

  def __init__(self):
    self.consumer_key = os.environ.get('etrade_consumer_key')
    self.consumer_secret = os.environ.get('etrade_consumer_secret')
 
  def oauth(self):
    """Allows user authorization for the sample application with OAuth 1"""
    etrade = OAuth1Service(
      name="etrade",
      consumer_key=self.consumer_key,
      consumer_secret=self.consumer_secret,
      request_token_url=const.REQUEST_TOKEN_URL,
      access_token_url=const.ACCESS_TOKEN_URL,
      authorize_url=const.AUTHORIZE_URL,
      base_url=const.BASE_URL)
    print("C")
    # Step 1: Get OAuth 1 request token and secret
    request_token, request_token_secret = etrade.get_request_token(
      params={"oauth_callback": "oob", "format": "json"})
 
    # Step 2: Go through the authentication flow. Login to E*TRADE.
    # After you login, the page will provide a text code to enter.
    authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
    print("Open the URL in the browser : ", end='')
    print(authorize_url)
    text_code = input("Please accept agreement and enter text code from browser: ")
 
    # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
    session = etrade.get_auth_session(request_token,
      request_token_secret,
      params={"oauth_verifier": text_code})
 
    return session
