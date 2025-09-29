# config.py
"""
Конфигурационный файл проекта.
Здесь задаются основные настройки: URL API бирж, интервалы обновления и другие параметры.
"""

# URL для API бирж (обновленные рабочие endpoints)
# Mexc
MEXC_TICKER_URL = "https://api.mexc.com/api/v3/ticker/24hr"
MEXC_ORDERBOOK_URL = "https://api.mexc.com/api/v3/depth"
MEXC_FUNDING_URL = "https://api.mexc.com/api/v3/premiumIndex"

# Bybit Spot  
BYBIT_TICKER_URL = "https://api.bybit.com/v5/market/tickers?category=spot"
BYBIT_ORDERBOOK_URL = "https://api.bybit.com/v5/market/orderbook?category=spot"
BYBIT_FUNDING_URL = "https://api.bybit.com/v5/market/funding/history?category=linear"

# Интервалы обновления данных (в секундах)
SPREAD_UPDATE_INTERVAL = 10       # Обновление спредов каждые 10 секунд
FUNDING_UPDATE_INTERVAL = 60      # Обновление фандинга каждые 60 секунд

# Список символов для мониторинга спредов
# Добавьте или удалите символы в зависимости от ваших потребностей
SYMBOLS_TO_MONITOR = [
    "BTCUSDT",     # Bitcoin
    "ETHUSDT",     # Ethereum
    "BNBUSDT",    # Binance Coin
    #"ADAUSDT",     # Cardano
    #"SOLUSDT",     # Solana
    #"DOTUSDT",     # Polkadot
    #"LINKUSDT",    # Chainlink
    #"MATICUSDT",   # Polygon
    #"AVAXUSDT",    # Avalanche
    #"ATOMUSDT",    # Cosmos
    #"ALGOUSDT",    # Algorand
    "XRPUSDT",     # Ripple
    #"LTCUSDT",     # Litecoin
    #"BCHUSDT",     # Bitcoin Cash
    #"EOSUSDT",     # EOS
    #"TRXUSDT",     # TRON
    #"XLMUSDT",     # Stellar
    #"VETUSDT",     # VeChain
    #"FILUSDT",     # Filecoin
    #"AAVEUSDT",    # Aave
    #"UNIUSDT",     # Uniswap
]
