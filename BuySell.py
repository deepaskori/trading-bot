from alpaca.data.live.stock import *
from alpaca.data.historical.stock import *
from alpaca.data.requests import *
from alpaca.data.timeframe import *
from alpaca.trading.client import *
from alpaca.trading.stream import *
from alpaca.trading.requests import *
from alpaca.trading.enums import *
from alpaca.common.exceptions import APIError
import TimeScale as TimeScale
import time

timescale = TimeScale.TimeScale()
if timescale.get_last_prices():
    ask_price, bid_price = timescale.get_last_prices()
    print("ask_price", ask_price)
    print("bid_price", bid_price)
    if timescale.get_last_bands():
        upper_band, lower_band = timescale.get_last_bands()
        print("upper_band", upper_band)
        print("lower_band", lower_band)
        

        api_key = "PKNNYCYZOPVK1V9ZFS6X"
        secret_key = "KxG2BMgxbbO5F1rVBk7jZhfwhoLfyKe08Ge2rIuh"
        paper = True
        trade_api_url = None
        symbol = "GOOG"

        trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=trade_api_url)
        print("ACCOUNT", trade_client.get_account())
        print("cash before", trade_client.get_account().cash)


        if bid_price <= lower_band and ask_price <= lower_band:
            req = MarketOrderRequest(
            symbol = symbol,
            notional = str(trade_client.get_account().cash),
            side = OrderSide.BUY,
            type = OrderType.MARKET,
            time_in_force = TimeInForce.DAY,
            )
            res = trade_client.submit_order(req)
            print("RESULT of buying:", res)
            print("cash after buying", trade_client.get_account().cash)

        time.sleep(20)

        if bid_price >= upper_band and ask_price >= upper_band:
            if trade_client.get_all_positions():
                req = ClosePositionRequest(percentage="100")
                res = trade_client.close_position(symbol_or_asset_id=symbol, close_options=req)
                print("RESULT of selling:", res)
                print("cash after selling", trade_client.get_account().cash)

