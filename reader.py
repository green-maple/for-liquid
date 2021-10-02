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

def get_logger(log_dir=None, log_file=None, prefix=None):
    logger = logging.getLogger('reader')
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
        fh = logging.handlers.RotatingFileHandler(log_file_full_name, mode='w', maxBytes=2000000, backupCount=5)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def read_partition(part, id=0):
    dataset = ds.dataset(part, format="parquet", partitioning="hive")
    try:
        if (id == 0):
            t = dataset.to_table().to_pandas() 
        else:
            t = dataset.to_table(filter=ds.field('account') == id).to_pandas() 
        logger.info(f'read partition from location: {part} \n {t}')
    except:
        logger.info(f'failed to read partition from location: {part} \n')
        t = None
    return t


def analyze():
    srcPath = base_dir
    df = read_partition(srcPath, 0) 
    logger.info(f'df: {df}')
    #df['date'] = pd.to_datetime(df['date'])
    df['date'] = pd.to_datetime(df['date'], unit='s')
    logger.debug(f'df: {df}')
    s = df['date']
    logger.debug(f's: {s}')
    #s1 = pd.date_range(s[0], s[4], freq='D').to_series()
    logger.info(f'dayofweek: %s', df['date'].dt.dayofweek)
    logger.info(f'dayname: %s', df['date'].dt.day_name())

    logger.info("\n------------")
    sum_of_quantity = df['quantity'].sum()
    logger.info(f'sum-of-quantity: {sum_of_quantity}')

    logger.info("\n------------")
    var_of_quantity = df.loc[:, "quantity"].var()
    logger.info(f'variance-of-quantity: {var_of_quantity}')

    accounts = df['account'].unique()
    unique_accounts = pd.Series(accounts)
    logger.info("\n------------")
    logger.info(type(unique_accounts))
    #print(f"unique accounts: {unique_accounts}")
    for account, value in unique_accounts.items():
        logger.info(f'account #: {account}, Value: {value}')

    logger.info("\n------------")
    products = df['product'].unique()
    unique_products = pd.Series(products)
    #print(f"unique products: {unique_products}")
    for product, value in unique_products.items():
        logger.info(f'product #: {product}, Value: {value}')

    row_count = len(df.index)
    logger.info(f'Number of rows: {row_count}')


if __name__ == '__main__':
    logger = get_logger('logs', 'reader.log')
    start_time = datetime.datetime.now() 
    iter = 1 
    while (not os.path.exists('parquet.stop')):
        logger.info(f'---------------------------iteration #: {iter} begins-----------------------------\n')
        df = read_partition(base_dir, 0)
        if df is None:
            while (df is None):
                df = read_partition(base_dir, 0)

        logger.info(f'----------------------------iteration #: {iter} ends------------------------------\n')
        iter = iter+1
#        logger.debug('sleep for 1 secs...')
#        time.sleep(1)
        
