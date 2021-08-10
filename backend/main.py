from database import DBConnection
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from stock_logic import StockLogic

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_connection = DBConnection() #use this connection class to query/insert


@app.get("/")
def read_root():
    return {"Hello world"}

@app.get("/get-stock-data/")
def read_root(stock_symbol: str, 
    start_date: Optional[datetime], 
    end_date: Optional[datetime]):

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    stock_logic = StockLogic(db_connection, stock_symbol, start_date, end_date) # this class will do all the logic
    some_data = stock_logic.getResponse()
    # all_db_data = db_connection.getAll()
    return some_data
    # return all_db_data
    # return some_data
    # return {"sym": stock_symbol, "st_d": start_date, "end_d": end_date}

