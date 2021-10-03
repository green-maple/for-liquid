# For-liquid
```
* This task demonstrates the ability to simulataneously read/write/append/mutate arrow/parquet files. 
* Solution:
* For mutation we are using `partition` based approach to localize the mutatation changes into the file
* For performing simultaneous read/write/mutate/append we make use of `partition` and do the file write in different file path and while read operation we check if the file has old `timestamp` then we first replace the mutated file and then do the reading.
* The Goal record schema:
   schema {
      optional binary field_id=-1 product (String);
      optional int64 field_id=-1 date;
      optional int64 field_id=-1 quantity;
      optional int64 field_id=-1 account;
  }
* The partitioning is done on the `account` field.
```


## Arrow/Parquet challenge

### Goal record
```
#### Example:
account     product              date                       quantity
1           apple                1631734436                 16
2           banana               1631664436                 2
3           grape                1631534436                 16
4           pineapple            1631434436                 2
5           guava                1631334436                 15
6           watermelon           1631234436                 2
7           plum                 1631134436                 12
```

### Recommendations
```
#### Example:
account     product              date                       quantity             WeekDay
1           apple                2021-09-15 19:33:56        16                   Wednesday
2           banana               2021-09-15 00:07:16        2                    Wednesday
3           grape                2021-09-13 12:00:36        16                   Monday
4           pineapple            2021-09-12 08:13:56        2                    Sunday
5           guava                2021-09-11 04:27:16        15                   Saturday
6           watermelon           2021-09-10 00:40:36        2                    Friday
7           plum                 2021-09-08 20:53:56        12                   Wednesday
```

### Arrow files:
#### arrow_service.py: 
```
* this file has code to read/write/mutate/append arrow data into the parquet files.
* this service keeps running and performing the following tasks:
  - read/write/mutate/append of data
  - analyze and compute statistics
  - show recommendations
* to stop this service you can create a file `arrow.stop` in the same directory
```

#### arrow_dash.py:
```
* this file contains dash app specific to arrow data reading and showing recommendations
```

### Parquet files:
#### parquet_service.py: 
```
* this file has code to read/write/mutate/append arrow data into the parquet files.
* this service keeps running and performing the following tasks:
  - read/write/mutate/append of data
  - analyze and compute statistics
  - show recommendations
* to stop this service you can create a file `parquet.stop` in the same directory
```

#### parquet_dash.py:
```
* this file contains dash app specific to parquet data reading and showing recommendations
```

####  reader.py:
```
* this file reads the data from the parquet file simultaneously while the backend services are writing/mutating/appending data to the same files
```


## Setup
python3 -m pip install -r requirements.txt


## Run

#### Arrow Service
```
python3 arrow_service.py
```

#### Parquet Service
```
python3 parquet_service.py
```

#### Reader
```
python3 reader.py
```

#### Dash visualization
Note: `arrow_dash.py` runs on port `8050` and `parquet_dash.py` run on port `8070`

```
python3 arrow_dash.py
```

```
python3 parquet_dash.py
```


## Usage
Step 1: 
```
Run either arrow_service.py or parquet_service.py (this will perform read/write/append/mutate tasks)
```
Step 2: 
```
Run reader.py (this will only do read task)
```
Step 3: 
```
To see the dash output run either arrow_dash.py or parquet_dash.py
```
