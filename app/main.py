from fastapi import FastAPI, Query
from typing import List
import pandas as pd
import os
from pathlib import Path

from .data_processing import (
    load_excel_data,
    cumulative_returns_and_alpha,
    exposure_difference,
)


app = FastAPI(title="Antipodes Financial APIs")

# Ensure Excel file path is correct -16/11/2025
BASE_DIR = Path(__file__).resolve().parents[1]
FILE_PATH = BASE_DIR / "Returns_and_Constituent_Data.xlsx"


returns_df, constituents_df = None, None

@app.on_event("startup")
def startup_event():
    global returns_df, constituents_df
    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError(f"Excel file not found: {FILE_PATH}")
    returns_df, constituents_df = load_excel_data(FILE_PATH)
    

@app.get("/returns")
def get_returns(
    as_of: str,
    month_period: List[int] = Query(default=[1,3,6,12], description="List of periods in months"),
    vehicle_col: str = "VehicleID",
    return_col: str = "Return",
    date_col: str = "Date",
    fund_id: str = Query(default="FUNDA", description="Fund VehicleID filter"),
    bench_id: str = Query(default="BENCHA", description="Benchmark VehicleID filter"),
    na_strategy: str = Query(default="keep", pattern="^(keep|zero|drop)$", description="NaN handling strategy"),
):
    result = cumulative_returns_and_alpha(
        returns_df,
        as_of_date=as_of,
        vehicle_col=vehicle_col,
        return_col=return_col,
        date_col=date_col,
        month_period=month_period,
        fund_id=fund_id,
        bench_id=bench_id,
        na_strategy=na_strategy
    )
    return {"results": result}


@app.get("/exposure")
def get_exposure(
    start_date: str,
    end_date: str,
    index_id: str = Query(default="BENCHA", description="Filter by IndexID"),
    date_col: str = "IndexDate",
    weight_col: str = "Weight",
    na_strategy: str = Query(default="keep", pattern="^(keep|zero|drop)$"),
):
    result = exposure_difference(
        constituents_df, start_date, end_date, date_col, weight_col, index_id, na_strategy
    )
    return {"results": result}
