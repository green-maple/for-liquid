# For-liquid

* Purpose: This task demonstrates the ability to simulataneously read/write/append/mutate arrow/parquet files.

* Solution:
  * For mutation we are using `partition` based approach to localize the mutatation changes into the file.
  * For performing simultaneous read/write/mutate/append we make use of `partition` and do the file 
    write in different file path and while read operation we check if the file has old `timestamp` then 
    we first replace the mutated file and then do the reading.

* The Goal record schema:
```
schema {
      optional binary field_id=-1 product (String);
      optional int64 field_id=-1 date;
      optional int64 field_id=-1 quantity;
      optional int64 field_id=-1 account;
  }
```
* The partitioning is done on the `account` field.
* The mutation is done on `quantity` field (partition=1).
* The partitioned files are stored in `/tmp/goal` directory.
* The mutated file for `account=1` partition is stored in `/tmp/mutate` directory and after mutation the partitioned
  file gets replaced within the `/tmp/goal` directory so that `reads` can see the mutated field values. This way all 
  operations (read, write, update, and mutation) are performed simulatneously.

## Arrow/Parquet challenge

### Goal record
```
Example:
account     product              date                       quantity
-------     -------              ------                     --------
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
Example:
account     product              date                       quantity             WeekDay
-------     -------              ------                     --------             --------
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
* this file has code implementation for read/write/mutate/append arrow data into the parquet files.
* this service keeps running and performing the following tasks:
  - read/write/mutate/append of data
  - analyze and compute statistics
  - show recommendations
* to stop this service you can create a file `arrow.stop` in the same directory
```
* data flow:
 * seed data is created using `pyarrow.array` arrays (for fields: `account`, `product`, `date`, and `quantity`) 
   and then transformed to `Record Batch` which in turn is converted to a `table` and then stored as partiotioned 
   dataset into the parquet file.

#### arrow_dash.py:
```
* this file contains dash app specific to arrow data reading and showing recommendations
* to see the mutated changes you can refresh the browser url (http://localhost:8050)
```

### Parquet files:
#### parquet_service.py: 
```
* this file has code implementation for read/write/mutate/append arrow data into the parquet files.
* this service keeps running and performing the following tasks:
  - read/write/mutate/append of data
  - analyze and compute statistics
  - show recommendations
* to stop this service you can create a file `parquet.stop` in the same directory
```
* data flow:
 * seed data is created using from pandas dataframe (for fields: `account`, `product`, `date`, and `quantity`) 
   and then converted to a `table` and then stored as partiotioned dataset into the parquet file.

#### parquet_dash.py:
```
* this file contains dash app specific to parquet data reading and showing recommendations
* to see the mutated changes you can refresh the browser url (http://localhost:8070)
```

####  reader.py:
```
* this file reads the data from the parquet file simultaneously while the backend services 
  are writing/mutating/appending data to the same files
* to stop the reader you can create a file `reader.stop` in the same directory
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
Run either arrow_service.py or parquet_service.py (to perform read/write/append/mutate tasks)
```
Step 2: 
```
Run reader.py (this will only do read task)
```
Step 3: 
```
To see the dash output run either arrow_dash.py or parquet_dash.py
```

## Dash Apps

### Parquet Dash Output
![Parquet](/images/parquet.png)

### Arrow Dash Output
![Arrow](/images/arrow.png)
