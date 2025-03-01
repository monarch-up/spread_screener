# exchanges.py
"""
Функции для взаимодействия с API бирж Mexc и Bybit.
Здесь выполняются реальные HTTP-запросы с использованием httpx.
Обратите внимание, что URL, параметры и обработка JSON-ответов могут потребовать корректировки
согласно актуальной документации бирж.
"""

import httpx
import asyncio
from typing import List
from config import (
    MEXC_TICKER_URL, MEXC_ORDERBOOK_URL, MEXC_FUNDING_URL,
    BYBIT_TICKER_URL, BYBIT_ORDERBOOK_URL, BYBIT_FUNDING_URL
)

async def fetch_mexc_data() -> List[dict]:
    """
    Получает данные тикера с Mexc.com.
    Возвращает список словарей с ключами: symbol, bid.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(MEXC_TICKER_URL)
        if response.status_code == 200:
            json_data = response.json()
            result = []
            # Предполагается, что данные находятся в поле "data"
            for item in json_data.get("data", []):
                # Нормализуем символ: например, "BTC_USDT" → "BTCUSDT"
                symbol = item.get("symbol", "").replace("_", "")
                try:
                    bid = float(item.get("bid", 0))
                except Exception:
                    bid = 0.0
                result.append({"symbol": symbol, "bid": bid})
            return result
        else:
            return []

async def fetch_bybit_data() -> List[dict]:
    """
    Получает данные тикера с Bybit Spot.
    Возвращает список словарей с ключами: symbol, ask.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(BYBIT_TICKER_URL)
        if response.status_code == 200:
            json_data = response.json()
            result = []
            # Предполагается, что данные находятся в поле "result"
            for item in json_data.get("result", []) or []:
                symbol = item.get("symbol", "")
                try:
                    ask = float(item.get("askPrice", 0))
                except Exception:
                    ask = 0.0
                result.append({"symbol": symbol, "ask": ask})
            return result
        else:
            return []

async def fetch_mexc_funding(symbol: str) -> float:
    """
    Получает ставку фандинга для инструмента с Mexc.com.
    URL строится с параметром symbol.
    """
    url = f"{MEXC_FUNDING_URL}?symbol={symbol}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            json_data = response.json()
            data = json_data.get("data", [])
            if data:
                try:
                    return float(data[0].get("fundingRate", 0))
                except Exception:
                    return 0.0
        return 0.0

async def fetch_bybit_funding(symbol: str) -> float:
    """
    Получает ставку фандинга для инструмента с Bybit.
    """
    url = f"{BYBIT_FUNDING_URL}?symbol={symbol}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            json_data = response.json()
            result = json_data.get("result", {})
            try:
                return float(result.get("funding_rate", 0))
            except Exception:
                return 0.0
        return 0.0

async def fetch_mexc_orderbook(symbol: str) -> dict:
    """
    Получает стакан ордеров с Mexc.com для заданного инструмента.
    Некоторые API требуют формат символа с разделителем (например, BTC_USDT).
    Здесь, если символ передан без "_", вставляем его.
    """
    if "_" not in symbol:
        # Простейшая логика преобразования (может требовать доработки для других монет)
        symbol_api = symbol[:3] + "_" + symbol[3:]
    else:
        symbol_api = symbol
    url = f"{MEXC_ORDERBOOK_URL}?symbol={symbol_api}&limit=10"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            json_data = response.json()
            return json_data.get("data", {})
        return {}

async def fetch_bybit_orderbook(symbol: str) -> dict:
    """
    Получает стакан ордеров с Bybit Spot для заданного инструмента.
    """
    url = f"{BYBIT_ORDERBOOK_URL}?symbol={symbol}&limit=10"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            json_data = response.json()
            return json_data.get("result", {})
        return {}
