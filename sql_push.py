import pandas as pd
import mysql.connector
# from mysql.connector import Error
from sqlalchemy import create_engine
import glob
import os
import xlrd


def connection():
  host = "localhost"
  user = "root"
  password = ""
  port = "3306"
  db = "amfi"
  try:
    conn = create_engine('mysql+mysqlconnector://'+user+":" +
                         password+"@"+host+":"+port+"/"+db)
    print("connected")
    return conn
  except Exception as e:
    print(e)
    return None


def schema(conn, column):
  query = "CREATE TABLE IF NOT EXISTS fund_performance_cat("+column+")"
  try:
    conn.execute(query)
    print("Table Creation!")
  except Exception as e:
    print(e)


def insert(conn, df):
  try:
    df.to_sql(name="fund_performance_cat", con=conn,
              if_exists="append", index=False)
    print("Inserted!")
  except Exception as e:
    print(e)


def connection_close(conn):
  print("connection closed")
  conn.dispose()


def create_DataFrame():
  PATH = "C:/Users/halde/OneDrive/Desktop/CelebalTech/Task6 (Selenium)/Files/"
  cols = [
      'Type', 'Category', 'Sub-Category', 'Scheme Name', 'Benchmark', 'NAV Date', 'NAV Regular', 'NAV Direct', 'Return 1 Year (%) Regular', 'Return 1 Year (%) Direct', 'Return 1 Year (%) Benchmark', 'Return 3 Year (%) Regular', 'Return 3 Year (%) Direct', 'Return 3 Year (%) Benchmark', 'Return 5 Year (%) Regular', 'Return 5 Year (%) Direct', 'Return 5 Year (%) Benchmark', 'Return 10 Year (%) Regular', 'Return 10 Year (%) Direct', 'Return 10 Year (%) Benchmark', 'Return Since Launch Regular', 'Return Since Launch Direct', 'Return Since Launch Benchmark', 'Daily AUM (Cr.)', 'Return 7 Days (%) Regular', 'Return 7 Days (%) Direct', 'Return 7 Days (%) Benchmark', 'Return 15 Days (%) Regular', 'Return 15 Days (%) Direct', 'Return 15 Days (%) Benchmark', 'Return 1 Month (%) Regular', 'Return 1 Month (%) Direct', 'Return 1 Month (%) Benchmark', 'Return 3 Month (%) Regular', 'Return 3 Month (%) Direct', 'Return 3 Month (%) Benchmark', 'Return 6 Month (%) Regular', 'Return 6 Month (%) Direct', 'Return 6 Month (%) Benchmark', 'Previous Month Closing AUM (Cr.)*', 'Previous Month Average AUM (Cr.)'
  ]
  df = pd.DataFrame(columns=cols)
  files = glob.glob(PATH + "\*.xls")

  for file in files:
    try:
      start_index = df.index[-1] + 1
    except:
      start_index = 0
    file_name = os.path.basename(file)
    file_path = PATH + file_name
    endType, primaryCategory, category = file_name.strip("'.xls").split('_')
    workbook = xlrd.open_workbook(file_path, ignore_workbook_corruption=True)
    temp_df = pd.read_excel(
        workbook, sheet_name="fund-performance",  skiprows=5)
    df = pd.concat([df, temp_df],  ignore_index=True)
    last_index = df.index[-1] + 1
    df['Type'][start_index:last_index] = str(endType)
    df['Category'][start_index:last_index] = str(primaryCategory)
    df['Sub-Category'][start_index:last_index] = str(category)

  print(df.shape)
  columns = tuple(df.columns)
  column_type = ["VARCHAR(255)"]*5 + ["DATE"] + ["FLOAT"]*35
  column = ""

  for i in range(len(columns)):
    if column == "":
      column = column+" `"+columns[i]+"` "+column_type[i]
    else:
      column = column+", `"+columns[i]+"` "+column_type[i]

  conn = connection()
  if conn:
    schema(conn, column)
    insert(conn, df)
    connection_close(conn)


if __name__ == "__main__":
  create_DataFrame()
