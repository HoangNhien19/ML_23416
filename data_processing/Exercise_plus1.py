import sqlite3
import pandas as pd

def top_customers_by_spending(db_path, n):
    query = """
        SELECT CustomerId AS ID,
               SUM(Total) AS Value
        FROM Invoice
        GROUP BY CustomerId
        ORDER BY Value DESC
        LIMIT ?;
    """
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query, conn, params=(n,))
    return df

db_path = '../databases/Chinook_Sqlite.sqlite'
n = int(input("Nhập số khách hàng thuộc top (n): "))

try:
    result = top_customers_by_spending(db_path, n)
    print(result)
except sqlite3.Error as e:
    print("Error occurred", e)
