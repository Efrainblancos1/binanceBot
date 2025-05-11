from binance.client import Client
import pandas as pd
import time

# Configura tus claves de Binance
API_KEY = 'lkNC9PuWPTpwkkkF3TWFIaZvesnCwI3IrJdcHxpxGymGibLhkIeQSVLZBnGIPoic'
API_SECRET = 'BIbrcXvxiRwuhGnrzzz1GhIspVHXomecVF31ZkZX8JKYfNVYJSKap8VF296xNgDK'
client = Client(API_KEY, API_SECRET)

# ==============================
# 👇 CONFIGURACIÓN MODIFICABLE 👇
# ==============================
TIPO_VELA = 'alcista'   # 'alcista' o 'bajista'
CANTIDAD_VELAS = 5      # Número de velas consecutivas
INTERVALO = '1d'        # Temporalidad: 1m, 5m, 15m, 1h, 4h, 1d, etc.

# ==============================
# FUNCIONES DEL BOT
# ==============================
def obtener_lista_pares_usdt():
    info = client.get_exchange_info()
    return [s['symbol'] for s in info['symbols'] if s['symbol'].endswith('USDT') and s['status'] == 'TRADING']

def obtener_klines(symbol, interval, limit=100):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'num_trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        df['open'] = df['open'].astype(float)
        df['close'] = df['close'].astype(float)
        return df
    except Exception as e:
        print(f"Error con {symbol}: {e}")
        return None

def tiene_n_velas_consecutivas(df, tipo='alcista', n=3):
    últimas = df.tail(n)
    if tipo == 'alcista':
        return all(últimas['close'] > últimas['open'])
    elif tipo == 'bajista':
        return all(últimas['close'] < últimas['open'])
    return False

# ==============================
# EJECUCIÓN DEL BOT
# ==============================
pares = obtener_lista_pares_usdt()
activos_filtrados = []

print(f"🔍 Buscando activos con {CANTIDAD_VELAS} velas {TIPO_VELA} en temporalidad {INTERVALO}...\n")

for par in pares:
    df = obtener_klines(par, INTERVALO, limit=CANTIDAD_VELAS + 5)
    if df is None or df.empty:
        continue

    if tiene_n_velas_consecutivas(df, tipo=TIPO_VELA, n=CANTIDAD_VELAS):
        activos_filtrados.append(par)

# ==============================
# RESULTADO
# ==============================
print(f"\n✅ Activos encontrados con {CANTIDAD_VELAS} velas {TIPO_VELA}:")
for activo in activos_filtrados:
    print(f" - {activo}")
