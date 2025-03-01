# config.py
"""
Конфигурационный файл проекта.
Здесь задаются основные настройки: URL API бирж, интервалы обновления и другие параметры.
"""

# URL для API бирж (эти адреса взяты как пример – проверьте их в официальной документации)
# Mexc
MEXC_TICKER_URL = "https://api.mexc.com/api/v2/market/ticker"
MEXC_ORDERBOOK_URL = "https://api.mexc.com/api/v2/market/depth"
MEXC_FUNDING_URL = "https://api.mexc.com/api/v2/futures/fundingRate"  # Предполагаемый URL для получения фандинга

# Bybit Spot
BYBIT_TICKER_URL = "https://api.bybit.com/spot/v1/ticker/24hr"
BYBIT_ORDERBOOK_URL = "https://api.bybit.com/spot/v1/depth"
BYBIT_FUNDING_URL = "https://api.bybit.com/v2/public/funding/prev_funding_rate"  # Предполагаемый URL для фандинга

# Интервалы обновления данных (в секундах)
SPREAD_UPDATE_INTERVAL = 10       # Обновление спредов каждые 10 секунд
FUNDING_UPDATE_INTERVAL = 60      # Обновление фандинга каждые 60 секунд
