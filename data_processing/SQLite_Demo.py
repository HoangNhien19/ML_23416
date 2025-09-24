import sqlite3
import pandas as pd

try:
    sqliteConnection = sqlite3.connect('../databases/Chinook_Sqlite.sqlite')
    cursor = sqliteConnection.cursor()
    print('DB Init')

    query = 'SELECT * FROM InvoiceLine LIMIT 5;'
    cursor.execute(query)

    col_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(cursor.fetchall(), columns=col_names)  # <- thêm columns
    print(df)

    # df = pd.DataFrame(cursor.fetchall())
    # print(df)
    cursor.close()

except sqlite3.Error as error:
    print('Error occurred -', error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')
