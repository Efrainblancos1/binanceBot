from binance.client import Client
import time
import pandas as pd
from ta.trend import EMAIndicator

API_KEY = 'lkNC9PuWPTpwkkkF3TWFIaZvesnCwI3IrJdcHxpxGymGibLhkIeQSVLZBnGIPoic'
API_SECRET = 'BIbrcXvxiRwuhGnrzzz1GhIspVHXomecVF31ZkZX8JKYfNVYJSKap8VF296xNgDK'

client = Client(API_KEY, API_SECRET)

def get_klines(symbol, interval, limit=100):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    return df

def trading_strategy(df):
    ema_fast = EMAIndicator(df['close'], window=9).ema_indicator()
    ema_slow = EMAIndicator(df['close'], window=21).ema_indicator()
    if ema_fast.iloc[-1] > ema_slow.iloc[-1] and ema_fast.iloc[-2] <= ema_slow.iloc[-2]:
        return 'BUY'
    elif ema_fast.iloc[-1] < ema_slow.iloc[-1] and ema_fast.iloc[-2] >= ema_slow.iloc[-2]:
        return 'SELL'
    return 'HOLD'

def place_order(symbol, side, quantity):
    order = client.create_order(
        symbol=symbol,
        side=side,
        type='MARKET',
        quantity=quantity
    )
    print(f"Order placed: {order}")

# Bucle principal
symbol = 'BTCUSDT'
quantity = 0.001  # Ajusta a tu balance

while True:
    df = get_klines(symbol, '5m', 100)
    signal = trading_strategy(df)
    print(f"Signal: {signal}")
    
    if signal == 'BUY':
        place_order(symbol, 'BUY', quantity)
    elif signal == 'SELL':
        place_order(symbol, 'SELL', quantity)

    time.sleep(300)  # Espera 5 minutos
