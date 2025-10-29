# #python -m pip install mysql-connector-python
# import mysql.connector
# import traceback
# import pandas as pd
# class Connector:
#     def __init__(self,server="localhost", port=3306, database="k23416_retail", username="root", password="@Obama123"):
#         self.server=server
#         self.port=port
#         self.database=database
#         self.username=username
#         self.password=password
#     def connect(self):
#         try:
#             self.conn = mysql.connector.connect(
#                 host=self.server,
#                 port=self.port,
#                 database=self.database,
#                 user=self.username,`
#                 password=self.password)
#             return self.conn
#         except:
#             self.conn=None
#             traceback.print_exc()
#         return None
#
#     def disConnect(self):
#         if self.conn != None:
#             self.conn.close()
#
#     def queryDataset(self, sql): #hàm trả về dataset
#         try:
#             cursor = self.conn.cursor()
#             cursor.execute(sql)
#             df = pd.DataFrame(cursor.fetchall()) # lấy toàn bộ dữ liệu MySQL trả về, dạng danh sách các tuple.
#
#             if not df.empty:
#                 df.columns=cursor.column_names
#             return df
#         except:
#             traceback.print_exc()
#         return None
#     def getTablesName(self): #tập các bảng
#         cursor = self.conn.cursor()
#         cursor.execute("Show tables;")
#         results=cursor.fetchall()
#         tablesName=[]
#         for item in results:
#             tablesName.append([tableName for tableName in item][0])
#         return tablesName
#     def fetchone(self,sql,val): #trả về một dòng dữ liệu
#         try:
#             cursor = self.conn.cursor()
#             cursor.execute(sql,val)
#             dataset = cursor.fetchone()
#             cursor.close()
#             return dataset
#         except:
#             traceback.print_exc()
#         return None
#     def fetchall(self,sql,val): #trả về một dòng dữ liệu
#         try:
#             cursor = self.conn.cursor()
#             cursor.execute(sql,val)
#             dataset = cursor.fetchone()
#             cursor.close()
#             return dataset
#         except:
#             traceback.print_exc()
#         return None


import mysql.connector
import traceback
import pandas as pd

class Connector:
    def __init__(self, server="localhost", port=3306, database="k23416_retail",
                 username="root", password="@Obama123"):
        self.server = server
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.server,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password
            )
            return self.conn
        except:
            self.conn = None
            traceback.print_exc()
        return None

    def disConnect(self):  # (giữ tên cũ để không ảnh hưởng nơi khác)
        if self.conn is not None:
            self.conn.close()

    def queryDataset(self, sql, params=None):  # thêm params cho linh hoạt
        cursor = None
        try:
            cursor = self.conn.cursor(buffered=True)  # <-- dùng buffered
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows)
            if not df.empty:
                df.columns = cursor.column_names
            return df
        except:
            traceback.print_exc()
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def getTablesName(self):  # tập các bảng
        cursor = None
        try:
            cursor = self.conn.cursor(buffered=True)  # <-- buffered
            cursor.execute("SHOW TABLES;")
            results = cursor.fetchall()
            tablesName = []
            for item in results:
                tablesName.append([tableName for tableName in item][0])
            return tablesName
        except:
            traceback.print_exc()
            return []
        finally:
            if cursor is not None:
                cursor.close()

    def fetchone(self, sql, val=None):  # trả về một dòng dữ liệu
        cursor = None
        try:
            cursor = self.conn.cursor(buffered=True)  # <-- buffered
            cursor.execute(sql, val)
            dataset = cursor.fetchone()
            return dataset
        except:
            traceback.print_exc()
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def fetchall(self, sql, val=None):  # trả về nhiều dòng dữ liệu
        cursor = None
        try:
            cursor = self.conn.cursor(buffered=True)  # <-- buffered
            cursor.execute(sql, val)
            datasets = cursor.fetchall()              # <-- đúng là fetchall()
            return datasets                           # trả về list (có thể rỗng)
        except:
            traceback.print_exc()
            return []
        finally:
            if cursor is not None:
                cursor.close()

    def insert_one(self, sql,val):
        cursor = None
        try:
            cursor = self.conn.cursor(buffered=True)  # <-- buffered
            cursor.execute(sql, val)
            self.conn.commit()
            result = cursor.rowcount
            return result
        except:
            traceback.print_exc()
            return []
        finally:
            if cursor is not None:
                cursor.close()


