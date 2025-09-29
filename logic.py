# logic.py
"""
Файл содержит бизнес-логику приложения.
Реализованы функции для:
- Периодического обновления данных (тикеров, фандинга)
- Вычисления спредов
- Сохранения истории спредов для построения графиков
"""

import asyncio
import time
from typing import Dict
from models import Instrument, ChartPoint
from exchanges import (
    fetch_mexc_data, fetch_bybit_data,
    fetch_mexc_funding, fetch_bybit_funding
)
from config import SYMBOLS_TO_MONITOR

# Глобальное хранилище актуальных данных по инструментам
instruments_data: Dict[str, Instrument] = {}

# Глобальное хранилище истории спредов (используется для графиков)
# Ключ – символ инструмента, значение – список объектов ChartPoint
spread_history: Dict[str, list[ChartPoint]] = {}

async def update_data():
    """
    Функция, выполняющая периодическое обновление данных:
    - Получает тикеры с Mexc и Bybit
    - Для каждого инструмента вычисляет спред (Mexc_bid - Bybit_ask)
    - Одновременно запрашивает фандинг для инструмента с обеих бирж
    - Обновляет глобальное хранилище instruments_data и сохраняет историю спредов
    """
    while True:
        try:
            mexc_data = await fetch_mexc_data()
            bybit_data = await fetch_bybit_data()

            for mexc_item in mexc_data:
                symbol = mexc_item["symbol"]
                
                # Фильтруем только символы из конфигурации
                if symbol not in SYMBOLS_TO_MONITOR:
                    continue
                    
                mexc_bid = mexc_item["bid"]

                # Ищем совпадение символа в данных Bybit
                bybit_item = next((item for item in bybit_data if item["symbol"] == symbol), None)
                if bybit_item:
                    bybit_ask = bybit_item["ask"]
                    spread = mexc_bid - bybit_ask if bybit_ask > 0 else 0


                    # Параллельно получаем ставки фандинга с Mexc и Bybit
                    funding_results = await asyncio.gather(
                        fetch_mexc_funding(symbol),
                        fetch_bybit_funding(symbol)
                    )
                    mexc_funding = funding_results[0]
                    bybit_funding = funding_results[1]

                    # Формируем объект инструмента
                    instrument = Instrument(
                        symbol=symbol,
                        mexc_bid=mexc_bid,
                        bybit_ask=bybit_ask,
                        spread=spread,
                        mexc_funding=mexc_funding,
                        bybit_funding=bybit_funding,
                        margin=None  # Логику расчёта маржи можно добавить при наличии соответствующих данных
                    )
                    instruments_data[symbol] = instrument

                    # Обновляем историю спредов для графика
                    timestamp = int(time.time())
                    point = ChartPoint(timestamp=timestamp, spread=spread)
                    if symbol not in spread_history:
                        spread_history[symbol] = []
                    spread_history[symbol].append(point)
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
        # Ждем указанный интервал перед следующим обновлением
        await asyncio.sleep(10)
