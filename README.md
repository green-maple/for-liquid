# For-liquid

## Arrow/Parquet challenge

### Goal record details

### Arrow files:
- arrow_service.py: 
* this file has code to read/write/mutate/append arrow data into the parquet files.
* this service keeps running and performing the following tasks:
  - read/write/mutate/append of data
  - analyze and compute statistics
  - show recommendations
* to stop this service you can create a file `arrow.stop` in the same directory

- arrow_dash.py: this shows 
* this file contains dash app specific to arrow data reading and showing recommendations

### Parquet files:
- arrow_service.py: 
* this file has code to read/write/mutate/append arrow data into the parquet files.
* this service keeps running and performing the following tasks:
  - read/write/mutate/append of data
  - analyze and compute statistics
  - show recommendations
* to stop this service you can create a file `arrow.stop` in the same directory

- arrow_dash.py: this shows 
* this file contains dash app specific to arrow data reading and showing recommendations

### Setup
python3 -m pip install -r requirements.txt
