from fastapi import FastAPI, Query
import pandas as pd
import numpy as np
from scipy.stats import gmean

#Read source excel sheets
def load_excel_data(filepath: str):
    returns_df = pd.read_excel(filepath, sheet_name="Returns")
    constituents_df = pd.read_excel(filepath, sheet_name="IndexConstituents")
    return returns_df, constituents_df

# Three strategies to handle nan value based on inputs and to calculate the cumulative geometric mean
# na_strategy options: 'keep', 'zero' and 'drop'
def geometric_cumulative_return(returns: pd.Series, na_strategy: str = "keep") -> float:
    if na_strategy == "zero":
        returns = returns.fillna(0)
    elif na_strategy == "drop":
        returns = returns.dropna()
    if returns.isna().any() or len(returns) == 0:
        return np.nan
        
    #https://www.investopedia.com/terms/g/geometricmean.asp  
    # μ geometric=[(1+R1)(1+R2)…(1+Rn)] power of 1/n −1       
    returns_count=len(returns)
    """Cumulative geometric mean (compounded return)."""
    return np.prod((1 + returns))**(1/returns_count) - 1
    
'''
#Alternatively method for average daily geometric mean return
def average_geometric_mean(returns: pd.Series, na_strategy: str = "drop") -> float:
    """Average geometric mean (per-day)."""
    
    if handle_nan == "drop":
        returns = returns.dropna()
    elif handle_nan == "zero":
        returns = returns.fillna(0)
    return gmean(1 + returns) - 1
'''   

def cumulative_returns_and_alpha(df, as_of_date, fund_col, bench_col, date_col, day_period, na_strategy="keep"):
    
    #Ensure the inputs is datetime format
    df[date_col] = pd.to_datetime(df[date_col])
    as_of_date = pd.to_datetime(as_of_date)
    output = []
    
    #The for loop may not be the most efficient approach for large datasets, but it serves the purpose for this task.
    for w in day_period:
        #Get start date based on entered day_period
        start_date = as_of_date - pd.Timedelta(days=w)
        #Filtering to only keep rows between the start date and as of date
        period_df = df[(df[date_col] >= start_date) & (df[date_col] <= as_of_date)]
        fund_return = geometric_cumulative_return(period_df[fund_col], na_strategy)
        bench_return = geometric_cumulative_return(period_df[bench_col], na_strategy)
        
        #Calculate the differences and check if any nan exist
        alpha = (fund_return - bench_return) if pd.notna(fund_return) and pd.notna(bench_return) else np.nan
        output.append({
            "as_of": as_of_date.strftime("%Y-%m-%d"),
            "Period": w,
            "FundReturn": fund_return,
            "BenchmarkReturn": bench_return,
            "Alpha": alpha
        })
    return output

# In this task the start_date: 1st of April 2025 and the end_date is 30th of June 2025
def exposure_difference(df, start_date, end_date, group_by, date_col, weight_col, na_strategy="keep"):
    df[date_col] = pd.to_datetime(df[date_col])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if na_strategy == "zero":
        df[weight_col] = df[weight_col].fillna(0)
    elif na_strategy == "drop":
        df = df.dropna(subset=[weight_col])

    start_df = df[df[date_col] == start_date]
    end_df= df[df[date_col] == end_date]

    start_sum = start_df.groupby(group_by, dropna=False)[weight_col].sum().reset_index().rename(columns={weight_col: "StartWeight"})
    end_sum = right_df.groupby(group_by, dropna=False)[weight_col].sum().reset_index().rename(columns={weight_col: "EndWeight"})

    merged = pd.merge(start_sum, end_sum, on=group_by, how="outer")
    merged["StartWeight"] = merged["StartWeight"].fillna(0)
    merged["EndWeight"] = merged["EndWeight"].fillna(0)
    merged["difference"] = merged["StartWeight"]- merged["EndWeight"]
    return merged.to_dict(orient="records")
