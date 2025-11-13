# antipodes_api

## Deliverable Criteria 

### 1. Using the Excel Data provided, create two REST API’s using the FastAPI Python Framework.  
  #### a. The provided Excel file contains two datasets; 
    i. Fund Returns Data – Daily Returns data of one fund and one benchmark 
    ii. Index Constituents – The constituent holdings of two index funds  

### 2. The two API’s should; 
 1.  Returns - Provide the cumulative geometric mean for the daily returns data for a range of periods, with the Alpha (difference) between the fund and benchmark. Eg. Give the cumulative geometric mean for Fund A and Benchmark A for a range of periods, as of 30th of June 2025
  
 2.  Exposure - Provide the difference in sum weight exposure for index constituents between two dates, for a specified grouping function. Eg. Give the sum weight exposure difference between the 1st of April 2025, and the 30th of June 2025, grouped by the Antipodes Region attribute 

### 3. All files should be stored within a public GitHub repository 
### 4. Create a GitHub Action which builds the Docker image, this doesn’t need to be pushed anywhere



## Directory Structure
```bash
antipodes_api
│   README.md
│   requirements.txt   
│   
└───app
│   │ main.py
│   │ data_processing.py
│   
└───.github
     └───workflows
         │ docker_build.yml
```

## Antipodes APIs
### HTTP Method: GET /returns Cumulative Returns and Alpha
### Query Parameters:

|Parameter   |	Type   |	Required |	  Default	      |             Description                  |
| :--------  |:------: |:------:   | :---------------:|-----------------------------------------:|
|as_of	     |str	     |  Yes	     |     -	          |  End date of the calculation (YYYY-MM-DD)|
|month_period|List[int]|	 No	     |   [1,3,6,12]	    |  List of periods in months               |
|vehicle_col |str	     |   No	     |   "VehicleID"	  |  Column name for vehicle ID              |
|return_col	 |str	     |   No	     |   "Return"	      |  Column name for return values           |
|date_col	   |str	     |   No	     |   "Date"	        |  Column name for date                    |
|fund_id	   |str	     |   No	     |   "FUNDA"	      |  Fund VehicleID filter                   |
|bench_id	   |str	     |   No	     |   "BENCHA"	      |  Benchmark VehicleID filter              |
|na_strategy |str	     |   No	     |   "keep"	        |  NaN handling strategy: keep, zero, drop |



### HTTP Method: GET /exposure — Exposure Differences
### Query Parameters:

|Parameter   |	Type   |	Required |	  Default	      |             Description                  |
| :--------  |:------: |:------:   | :---------------:|-----------------------------------------:|
|start_date  |str	     |   Yes	   |     -	          |  Start date (YYYY-MM-DD)                 |
|end_date    |str      |	 Yes	   |     -      	    |  End date (YYYY-MM-DD)                   |
|index_id    |str	     |   No	     |   "BENCHA"	      |  IndexID to filter                       |
|date_col	   |str	     |   No	     |   "IndexDate"    |  Column name for date                    |
|weight_col	 |str	     |   No	     |   "weight"	      |  Column name for weight                  |
|na_strategy |str	     |   No	     |   "keep"	        |  NaN handling strategy: keep, zero, drop |






