import datetime
from datetime import date
import awswrangler as wr
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds
from pyarrow import fs

import tempfile
import pathlib

import random
import time
import os
from os import listdir
from os.path import isfile, join

import logging
import logging.handlers
from shutil import copy2

base_dir = pathlib.Path(tempfile.gettempdir()) / "goal"
mutate_dir = pathlib.Path(tempfile.gettempdir()) / "mutate"

def get_logger(log_dir=None, log_file=None, prefix=None):
    logger = logging.getLogger('arrow_service')
    logger.setLevel(logging.INFO)
    head = '%(asctime)-15s - %(name)s - %(levelname)s (%(threadName)-9s) - %(message)s'
    formatter = logging.Formatter(head)

    if log_dir:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        if not log_file:
            log_file = (prefix if prefix else '') + datetime.now().strftime('_%Y_%m_%d-%H_%M.log')
            log_file = log_file.replace('/', '-')
        else:
            log_file = log_file
        log_file_full_name = os.path.join(log_dir, log_file)

    if log_file:
        fh = logging.handlers.RotatingFileHandler(log_file_full_name, mode='w', maxBytes=5000000, backupCount=5)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def create_data():
    data = [
        pa.array([1, 2, 3, 4, 5, 6, 7]),
        pa.array(["apple", "banana", "grape", "pineapple", "guava", "watermelon", "plum"]),
        pa.array([1631734436, 1631664436, 1631534436, 1631434436, 1631334436, 1631234436, 1631134436]),
        pa.array([random.randint(1, 20), random.randint(1, 10), random.randint(10, 20), random.randint(1, 10), random.randint(10, 30), random.randint(1, 10), random.randint(10, 20)])
    ]
    return data


def create_batch():
    data = create_data()
    batch = pa.RecordBatch.from_arrays(data, ["account", "product", "date", "quantity"])
#    print(batch.schema)
    return batch


def write_to_s3(df):
    wr.s3.to_parquet(df, path)


def write_partition(d="test_1"):
    src_dir = base_dir / d 
    logger.debug(f'src_dir: %s', str(src_dir))
    os.makedirs(src_dir, exist_ok=True)
    batch = create_batch()
    table = pa.Table.from_batches([batch]*1)

    part = ds.partitioning(pa.schema([("account", pa.int64())]), flavor="hive")
    ds.write_dataset(table, src_dir, format="parquet", partitioning=part)
    
    dataset = ds.dataset(src_dir, partitioning=part)
    t = dataset.to_table(filter=ds.field('account') == 1).to_pandas()
    logger.info(f'written partition dataset at location: {src_dir} \n{t}') 

    ds1 = ds.dataset(str(src_dir), format="parquet", partitioning=part)
    for i in ds1.files:
        logger.debug(f'files: %s', i)


def append_partition(d="test_1"):
    write_new_partition(d)


def mutate_partition(d="test_1"):
    d = mutate_dir / d
    write_new_partition(d)


def write_new_partition(d="test_1"):
    src_dir = base_dir / d
    os.makedirs(src_dir, exist_ok=True)
    df = create_row_df()
    table = pa.Table.from_pandas(df)
    part = ds.partitioning(pa.schema([("account", pa.int64())]), flavor="hive")    
    ds.write_dataset(table, src_dir, format="parquet", partitioning=part)
    
    dataset = ds.dataset(src_dir, partitioning=part)
    t = dataset.to_table(filter=ds.field('account') == 1).to_pandas()
    logger.info(f'written new partition dataset at location: {src_dir} \n{t}') 


def read_partition(part, id=0):
    dataset = ds.dataset(part, format="parquet", partitioning="hive")
    if (id == 0):
        t = dataset.to_table().to_pandas() 
    else:
        t = dataset.to_table(filter=ds.field('account') == id).to_pandas() 
    logger.info(f'reading partition from location: {part} \n {t}') 
    return t


def read_partition_table(part, id=0):
    dataset = ds.dataset(part, format="parquet", partitioning="hive")
    if (id == 0):
        t = dataset.to_table() 
    else:
        t = dataset.to_table(filter=ds.field('account') == id) 
    logger.info(f'reading partition from location: {part} \n {t}') 
    return t


def read_partition_data(id=0):
    # Check file modification time
    check_file_time(id)


def check_file_time(id=0):
    # Check file modification time
    dstFilePath = f'{base_dir}/test_1/account={id}'
    logger.debug(f'dstFilePath: %s', dstFilePath)
    dstFileTime, dfp = get_file_time(dstFilePath)
    if (dstFileTime > 0):
        logger.debug(f'dstFileTime: %s', str(dstFileTime))
        read_partition(dstFilePath) 
    
        srcFilePath = f'{mutate_dir}/test_1/account={id}'
        logger.debug(f'srcFilePath: %s', srcFilePath)
        srcFileTime, sfp = get_file_time(srcFilePath)
        if (srcFileTime > 0):
            logger.debug(f'srcFileTime: %s', str(srcFileTime))
            read_partition(srcFilePath) 
            if (srcFileTime > dstFileTime):
                file_replace(sfp, dfp)


def get_file_time(filePath):
    fileModTime = 0
    try:
        fileName = [f for f in listdir(filePath) if isfile(join(filePath, f))]
        if ((fileName) and (fileName is not None)):
            logger.debug(f'FileName: %s', str(fileName[0]))
            filePath = filePath + "/" + str(fileName[0])
            logger.debug(f'FilePath: %s', filePath)
            fileModTime = os.path.getmtime(str(filePath))
            logger.debug(f'file-mod-time: %s', str(fileModTime))
    except FileNotFoundError:
        logger.info(f'file not found!')
    return fileModTime, filePath


def file_replace(src, dst):
    copy2(src, dst)
    logger.info(f'file replaced successfully!')


def create_row_df():
    account = [1]
    product = ["apple"]
    date = [1632808217] 
    quantity = [random.randint(1, 20)]
    
    df1 = pd.DataFrame({
        "account": account,
        "product": product,
        "date": date,
        "quantity": quantity
    })
    return df1


def read_from_s3():
#    path1 = f"s3://unravel-saas-demo/test/my.parquet"
    return wr.s3.read_parquet([path1])

#writer = None
#writer = write_to_s3(writer)
#writer = write(writer)
#print("s3 data: " + str(read_from_s3()))
#print(str(read_from_s3()))


def compute(data):
    logger.info('---- Compute values ----')
    logger.debug(f'####### data: {data}')

    # Get field value count
    count = pa.compute.count(data[0])
    logger.info(f'count: {count}')

    # Get mean of array data
    mean = pa.compute.mean(data[2])
    logger.info(f'mean: {mean}')

    # Get sum of 'Quantity' field
    sum = pa.compute.sum(data[2])
    logger.info(f'sum: {sum}')

    # Get variance of quantity
    var = pa.compute.variance(data[2])
    logger.info(f'var: {var}')

    # Get number of unique account
    uniq_account = pa.compute.unique(data[3])
    logger.info(f'unique account: {uniq_account}')

    # Get number of unique product
    uniq_product = pa.compute.unique(data[0])
    logger.info(f'unique product: {uniq_product}')


def analyze():
    srcPath = base_dir
    t = read_partition_table(srcPath, 0)
    logger.info(f'---- Goal recommendations ---\n%s', t)
    
    compute(t)
    df = t.to_pandas() 
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df['WeekDay'] = df['date'].dt.day_name()
    logger.info(f'---- Goal recommendations ---\n%s', df)


if __name__ == '__main__':
    logger = get_logger('logs', 'arrow_service.log')
    start_time = datetime.datetime.now() 
    iter = 0
    dir_iter = 0
    logger.info('Starting task: Read/Write/Append/Mutate Goal record...')
    write_partition()
    write_new_partition()

    while (not os.path.exists('arrow.stop')):
        iter = iter + 1
        logger.info(f'---------------------------iteration #: {iter} begins-----------------------------\n')
        elapsed_time = datetime.datetime.now() - start_time
        if (elapsed_time.seconds > 1):
            logger.info('==> elapsed 1 sec, do append and mutate tasks...')
            dir_iter = dir_iter + 1
            d = f'test_{dir_iter}'
            append_partition(d)
            mutate_partition("test_1")
            analyze()
            start_time = datetime.datetime.now()
            logger.info('==> append and mutate tasks completed successfully...')

        read_partition_data(1)

        logger.debug('sleep for 1 sec...')
        logger.info(f'----------------------------iteration #: {iter} ends------------------------------\n')
        time.sleep(1)
