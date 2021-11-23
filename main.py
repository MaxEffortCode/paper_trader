import alpaca_trade_api as tradeapi

#api key PKQJSU27J89VZJE92N1J
#secret key zex4T98XNcnj4UoVSCPbmVAelkvvAhuboSFeAZQN
api = tradeapi.REST(
        'PKQJSU27J89VZJE92N1J',
        'zex4T98XNcnj4UoVSCPbmVAelkvvAhuboSFeAZQN',
        'https://paper-api.alpaca.markets', api_version='v2'
)
        
# Submit a market order to buy 1 share of Apple at market price
api.submit_order(
    symbol='AAPL',
    qty=1,
    side='buy',
    type='market',
    time_in_force='gtc'
)