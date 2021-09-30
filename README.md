# For-liquid

## Arrow/Parquet challenge

### Goal record
#### Example: <br />
   account     product        date  quantity <br />
0        1       apple  1631734436        16 <br />
1        2      banana  1631664436         2 <br />
2        3       grape  1631534436        16 <br />
3        4   pineapple  1631434436         2 <br />
4        5       guava  1631334436        15 <br />
5        6  watermelon  1631234436         2 <br />
6        7        plum  1631134436        12 <br />

### Recommendations
#### Example: <br />
   account     product                date  quantity    WeekDay <br />
0        1       apple 2021-09-15 19:33:56        16  Wednesday <br />
1        2      banana 2021-09-15 00:07:16         2  Wednesday <br />
2        3       grape 2021-09-13 12:00:36        16     Monday <br />
3        4   pineapple 2021-09-12 08:13:56         2     Sunday <br />
4        5       guava 2021-09-11 04:27:16        15   Saturday <br />
5        6  watermelon 2021-09-10 00:40:36         2     Friday <br />
6        7        plum 2021-09-08 20:53:56        12  Wednesday <br />

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
