# models.py
"""
Файл содержит определения моделей данных с использованием Pydantic.
Модели описывают:
- Информацию по инструментам (тикер, спред, фандинг, маржа)
- Точки для графика спреда
- Формат данных для стакана ордеров
"""

from pydantic import BaseModel
from typing import List, Optional

class Instrument(BaseModel):
    symbol: str            # Символ инструмента, например, "BTCUSDT"
    mexc_bid: float        # Цена покупки (Bid) на бирже Mexc
    bybit_ask: float       # Цена продажи (Ask) на бирже Bybit
    spread: float          # Вычисленный спред: разница между Mexc_bid и Bybit_ask
    mexc_funding: Optional[float] = None    # Ставка фандинга с Mexc
    bybit_funding: Optional[float] = None   # Ставка фандинга с Bybit
    margin: Optional[float] = None          # Минимальная маржа (рассчитывается при наличии данных)

class ChartPoint(BaseModel):
    timestamp: int  # Временная метка (UNIX-время)
    spread: float   # Значение спреда в этот момент времени

class ChartData(BaseModel):
    symbol: str              # Символ инструмента
    period: str              # Временной интервал графика ("1m", "5m", "1h", "4h")
    data: List[ChartPoint]   # Список точек графика

class OrderBookEntry(BaseModel):
    price: float   # Цена заявки
    volume: float  # Объем заявки

class OrderBook(BaseModel):
    exchange: str                # Название биржи ("mexc" или "bybit")
    symbol: str                  # Символ инструмента
    bids: List[OrderBookEntry]   # Список заявок на покупку (Bid)
    asks: List[OrderBookEntry]   # Список заявок на продажу (Ask)
