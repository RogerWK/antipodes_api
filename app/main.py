from fastapi import FastAPI, Query
from typing import List
import pandas as pd
from .data_processing import (
    load_excel_data,
    cumulative_returns_and_alpha,
    exposure_difference,
)

app = FastAPI(title="Antipodes Financial APIs")

FILE_PATH = "Returns_and_Constituent_Data.xlsx"
returns_df, constituents_df = load_excel_data(FILE_PATH)


@app.get("/returns")
def get_returns(
    as_of: str,
    day_period: List[int] = Query(default=[30, 90, 180]),
    fund_col: str = "Fund",
    bench_col: str = "Benchmark",
    date_col: str = "Date",
    na_strategy: str = Query(default="keep", regex="^(keep|zero|drop)$"),
):
    result = cumulative_returns_and_alpha(
        returns_df, as_of, fund_col, bench_col, date_col, day_period, na_strategy
    )
    return {"results": result}


@app.get("/exposure")
def get_exposure(
    start_date: str,
    end_date: str,
    group_by: str = "Antipodes Region",
    date_col: str = "Date",
    weight_col: str = "Weight",
    na_strategy: str = Query(default="keep", regex="^(keep|zero|drop)$"),
):
    result = exposure_difference(
        constituents_df, start_date, end_date, group_by, date_col, weight_col, na_strategy
    )
    return {"results": result}
