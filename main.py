# From:  https://nexusfission.com/2023/11/14/etrade-api-setup-using-python-automation-oauth-1-0-explained/
import os
from auth import EtradeAuth
from market import EtradeMarket
 
if __name__ == "__main__":
 
  print("Setting up Auth : ", end='')
  auth = EtradeAuth()
  session = auth.oauth()
  if session:
    print("SUCCESS")
  else:
    print("FAILED")
    exit()
 
  market = EtradeMarket(session)
  print(market.get_quotes('AAPL'))