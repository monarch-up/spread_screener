# app.py
"""
Основной файл приложения.
Настраивается FastAPI сервер с использованием lifespan-обработчика для управления событиями старта/завершения.
Определены API эндпоинты, включая эндпоинт для отображения HTML-страницы (dashboard).
"""

import asyncio
import time
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from typing import List, Optional
import uvicorn

from models import Instrument, ChartData, ChartPoint, OrderBook, OrderBookEntry
from logic import update_data, instruments_data, spread_history
from exchanges import fetch_mexc_orderbook, fetch_bybit_orderbook

# Настройка шаблонов. Папка "templates" должна находиться в корневой директории проекта.
templates = Jinja2Templates(directory="templates")

# Lifespan-обработчик: запуск фоновой задачи при старте и отмена при завершении
@asynccontextmanager
async def lifespan(app: FastAPI):
    update_task = asyncio.create_task(update_data())
    yield
    update_task.cancel()

# Создаем объект FastAPI с lifespan-обработчиком
app = FastAPI(title="Скринер спредов для Mexc и Bybit Spot", lifespan=lifespan)

# Эндпоинт для отображения HTML-страницы дашборда
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """
    Эндпоинт для отображения HTML-страницы дашборда с таблицей.
    При необходимости можно передать динамические данные в шаблон.
    """
    data = list(instruments_data.values())  # Можно использовать data для динамического наполнения шаблона
    return templates.TemplateResponse("dashboard.html", {"request": request, "data": list(instruments_data.values())})



@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "data": list(instruments_data.values())})




@app.get("/api/spreads", response_model=List[Instrument])
async def get_spreads():
    """
    Эндпоинт для получения списка инструментов со спредами между Mexc и Bybit.
    """
    return list(instruments_data.values())

@app.get("/api/funding", response_model=List[Instrument])
async def get_funding_info():
    """
    Эндпоинт для получения информации по фандингу для каждого инструмента.
    """
    return list(instruments_data.values())

@app.get("/api/chart/{symbol}", response_model=ChartData)
async def get_chart_data(symbol: str, period: str = Query("1m", pattern="^(1m|5m|1h|4h)$")):
    """
    Эндпоинт для получения данных графика спреда для указанного инструмента.
    Фильтрует историю спредов за выбранный период.
    """
    current_time = int(time.time())
    period_seconds = {"1m": 60, "5m": 300, "1h": 3600, "4h": 14400}
    window = period_seconds.get(period, 60)
    points = spread_history.get(symbol, [])
    filtered_points = [pt for pt in points if current_time - pt.timestamp <= window]
    return ChartData(symbol=symbol, period=period, data=filtered_points)

@app.get("/api/orderbook/{exchange}/{symbol}", response_model=OrderBook)
async def get_orderbook(exchange: str, symbol: str):
    """
    Эндпоинт для получения стакана ордеров для указанного инструмента и биржи.
    """
    if exchange.lower() == "mexc":
        data = await fetch_mexc_orderbook(symbol)
        bids = [OrderBookEntry(price=float(bid[0]), volume=float(bid[1])) for bid in data.get("bids", [])]
        asks = [OrderBookEntry(price=float(ask[0]), volume=float(ask[1])) for ask in data.get("asks", [])]
        return OrderBook(exchange="mexc", symbol=symbol, bids=bids, asks=asks)
    elif exchange.lower() == "bybit":
        data = await fetch_bybit_orderbook(symbol)
        bids = [OrderBookEntry(price=float(bid[0]), volume=float(bid[1])) for bid in data.get("bids", [])]
        asks = [OrderBookEntry(price=float(ask[0]), volume=float(ask[1])) for ask in data.get("asks", [])]
        return OrderBook(exchange="bybit", symbol=symbol, bids=bids, asks=asks)
    else:
        return OrderBook(exchange=exchange, symbol=symbol, bids=[], asks=[])

@app.get("/api/instruments", response_model=List[Instrument])
async def filter_sort_instruments(
    sort_by: Optional[str] = Query(None, description="Поле для сортировки: spread, funding, margin"),
    min_margin: Optional[float] = Query(None, description="Фильтр по минимальной марже (в процентах)"),
    min_spread: Optional[float] = Query(None, description="Фильтр по минимальному значению спреда"),
    funding_type: Optional[str] = Query(None, description="Фильтр по типу фандинга: positive или negative")
):
    """
    Эндпоинт для фильтрации и сортировки списка инструментов.
    """
    instruments = list(instruments_data.values())
    if min_margin is not None:
        instruments = [inst for inst in instruments if inst.margin is not None and inst.margin >= min_margin]
    if min_spread is not None:
        instruments = [inst for inst in instruments if inst.spread >= min_spread]
    if funding_type:
        if funding_type == "positive":
            instruments = [inst for inst in instruments if (inst.mexc_funding or 0) > 0 and (inst.bybit_funding or 0) > 0]
        elif funding_type == "negative":
            instruments = [inst for inst in instruments if (inst.mexc_funding or 0) < 0 and (inst.bybit_funding or 0) < 0]
    if sort_by:
        if sort_by == "spread":
            instruments.sort(key=lambda x: x.spread)
        elif sort_by == "funding":
            instruments.sort(key=lambda x: (x.mexc_funding or 0) + (x.bybit_funding or 0))
        elif sort_by == "margin":
            instruments.sort(key=lambda x: x.margin if x.margin is not None else 0)
    return instruments

if __name__ == "__main__":
    import os
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=os.getenv("DEBUG", "false") == "true")

