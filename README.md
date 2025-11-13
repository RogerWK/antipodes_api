# antipodes_api

Deliverable Criteria 
1. Using the Excel Data provided, create two REST API’s using the FastAPI Python 
Framework.  
a. The provided Excel file contains two datasets; 
i. Fund Returns Data – Daily Returns data of one fund and one 
benchmark 
ii. Index Constituents – The constituent holdings of two index funds  
2. The two API’s should; 
a. Returns - Provide the cumulative geometric mean for the daily returns data 
for a range of periods, with the Alpha (difference) between the fund and 
benchmark. Eg. Give the cumulative geometric mean for Fund A and 
Benchmark A for a range of periods, as of 30th of June 2025


b. Exposure - Provide the difference in sum weight exposure for index 
constituents between two dates, for a specified grouping function. Eg. Give 
the sum weight exposure difference between the 1st of April 2025, and the 
30th of June 2025, grouped by the Antipodes Region attribute 
4. All files should be stored within a public GitHub repository 
5. Create a GitHub Action which builds the Docker image, this doesn’t need to be 
pushed anywhere

app/main.py-- FastAPI with two endpoints:

a.Returns - GET /returns
Query params:
as_of (YYYY-MM-DD) — required
day_period (list of ints) — default [30,90,180]
fund_col (str) — default "Fund"
bench_col (str) — default "Benchmark"
date_col (str) — default "Date"
na_strategy — keep|zero|drop
Response: { "results": [ ... ] }

b. Exposure - GET /exposure
Query params:
start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), group_by (str) — required
date_col (str) default "Date", weight_col default "Weight", na_strategy
Response: { "results": [ {group_by, sum_weight_left, sum_weight_right, difference}, ... ] }
