import chardet
import pandas
import re

def get_encoding(dataset, default_encoding='latin1', num_bytes=100000):
  encoding = default_encoding
  with open(dataset, 'rb') as raw:
    result = chardet.detect(raw.read(num_bytes))
    if result['encoding'] != 'ascii':
      encoding = result['encoding']
  return encoding

def is_unnamed_col(col_name):
  unnamed_re = r'Unnamed:\s\d+'
  return (col_name is None or col_name == '' or re.match(unnamed_re, col_name))

def read_dataset(dataset, ignore_unnamed_cols=True):
  encoding = get_encoding(dataset)
  print(f"Reading dataset '{dataset}' with encoding '{encoding}'")
  
  usecols = None
  if ignore_unnamed_cols:
    cols = list(pandas.read_csv(dataset, encoding=encoding, nrows=1))
    usecols = [c for c in cols if not is_unnamed_col(c)]

  df = pandas.read_csv(dataset, encoding=encoding, usecols=usecols)
  return df
