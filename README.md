# For-liquid

## Arrow/Parquet challenge

### Goal record
#### Example: <br />
   account&nbsp;&nbsp;     product&nbsp;&nbsp;        date&nbsp;&nbsp;  quantity <br />
0&nbsp;&nbsp;        1&nbsp;&nbsp;       apple&nbsp;&nbsp;  1631734436&nbsp;&nbsp;        16 <br />
1&nbsp;&nbsp;        2&nbsp;&nbsp;      banana&nbsp;&nbsp;  1631664436&nbsp;&nbsp;         2 <br />
2&nbsp;&nbsp;        3&nbsp;&nbsp;       grape&nbsp;&nbsp;  1631534436&nbsp;&nbsp;        16 <br />
3&nbsp;&nbsp;        4&nbsp;&nbsp;   pineapple&nbsp;&nbsp;  1631434436&nbsp;&nbsp;         2 <br />
4&nbsp;&nbsp;        5&nbsp;&nbsp;       guava&nbsp;&nbsp;  1631334436&nbsp;&nbsp;        15 <br />
5&nbsp;&nbsp;        6&nbsp;&nbsp;  watermelon&nbsp;&nbsp;  1631234436&nbsp;&nbsp;         2 <br />
6&nbsp;&nbsp;        7&nbsp;&nbsp;        plum&nbsp;&nbsp;  1631134436&nbsp;&nbsp;        12 <br />

### Recommendations
#### Example: <br />
   account&nbsp;&nbsp;     product&nbsp;&nbsp;                date&nbsp;&nbsp;  quantity&nbsp;&nbsp;    WeekDay&nbsp;&nbsp; <br />
0&nbsp;&nbsp;        1&nbsp;&nbsp;       apple&nbsp;&nbsp; 2021-09-15 19:33:56&nbsp;&nbsp;        16&nbsp;&nbsp;  Wednesday <br />
1&nbsp;&nbsp;        2&nbsp;&nbsp;      banana&nbsp;&nbsp; 2021-09-15 00:07:16&nbsp;&nbsp;         2&nbsp;&nbsp;  Wednesday <br />
2&nbsp;&nbsp;        3&nbsp;&nbsp;       grape&nbsp;&nbsp; 2021-09-13 12:00:36&nbsp;&nbsp;        16&nbsp;&nbsp;     Monday <br />
3&nbsp;&nbsp;        4&nbsp;&nbsp;   pineapple&nbsp;&nbsp; 2021-09-12 08:13:56&nbsp;&nbsp;         2&nbsp;&nbsp;     Sunday <br />
4&nbsp;&nbsp;        5&nbsp;&nbsp;       guava&nbsp;&nbsp; 2021-09-11 04:27:16&nbsp;&nbsp;        15&nbsp;&nbsp;   Saturday <br />
5&nbsp;&nbsp;        6&nbsp;&nbsp;  watermelon&nbsp;&nbsp; 2021-09-10 00:40:36&nbsp;&nbsp;         2&nbsp;&nbsp;     Friday <br />
6&nbsp;&nbsp;        7&nbsp;&nbsp;        plum&nbsp;&nbsp; 2021-09-08 20:53:56&nbsp;&nbsp;        12&nbsp;&nbsp;  Wednesday <br />

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
