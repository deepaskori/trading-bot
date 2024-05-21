import websocket
import json
import TimeScale as TimeScale
from datetime import datetime, timezone

class WebSocket():
    headers = {
    "APCA-API-KEY-ID": "PKNNYCYZOPVK1V9ZFS6X",
    "APCA-API-SECRET-KEY": "KxG2BMgxbbO5F1rVBk7jZhfwhoLfyKe08Ge2rIuh"
    }

    ws_url = "wss://stream.data.alpaca.markets/v2/iex"

    #for testing
    # ws_url = "wss://stream.data.alpaca.markets/v2/test"



    def __init__(self, message):
        self.message = message

    def on_message(self, ws, message):
        
        data = json.loads(message)
        if data[0]['T'] == 'q':
            symbol = data[0]["S"]
            bid = data[0]["bp"]
            ask = data[0]["ap"]
            t = data[0]["t"]
            dt = datetime.fromisoformat(t[:26])  
            utc_dt = dt.replace(tzinfo=timezone.utc)
            timescale.insert_row_into_batch((utc_dt, symbol, ask, bid))
            print(f"{symbol} has bid price of {bid} and ask price of {ask} at time {t}")
                
        else:
            print(f"Received message: {message}")

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws):
        timescale.conn.close()
        timescale.conn.cursor.close()
        print("Connection closed")

    def on_open(self, ws):
        print("Connection opened")
        ws.send(json.dumps(self.message))

if __name__ == "__main__":
    test = WebSocket({"action":"subscribe","quotes":["GOOG"]})

    #for testing
    # test = WebSocket({"action":"subscribe","quotes":["FAKEPACA"]})
    
    ws = websocket.WebSocketApp(test.ws_url,
                                header=test.headers,
                                on_message=test.on_message,
                                on_error=test.on_error,
                                on_close=test.on_close)
    timescale = TimeScale.TimeScale()
    ws.on_open = test.on_open
    ws.run_forever()