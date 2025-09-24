import sqlite3
import pandas as pd

N =  int(input("Nhập số khách hàng thuộc top (n):"))
sqliteConnection = None
try:
    sqliteConnection = sqlite3.connect('../databases/Chinook_Sqlite.sqlite')
    print('DB Init')

    query = f"""
        SELECT
            i.CustomerId AS ID,
            SUM(il.UnitPrice * il.Quantity) AS Value
        FROM Invoice AS i
        JOIN InvoiceLine AS il
            ON i.InvoiceId = il.InvoiceId
        GROUP BY i.CustomerId
        ORDER BY Value DESC
        LIMIT {N};
    """

    df_top_customers = pd.read_sql_query(query, sqliteConnection)
    print(df_top_customers)

except sqlite3.Error as error:
    print("Error occurred -", error)

finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("SQLite Connection closed")
