### Thêm mới dữ liệu MySQLServer

import mysql.connector

server="localhost"
port=3306
database="studentmanagement"
username="root"
password="@Obama123"

conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)

# ############ 3.1
# cursor = conn.cursor()
#
# sql="insert into student (code,name,age) values (%s,%s,%s)"
#
# val=("sv07","Trần Duy Thanh",45)
#
# cursor.execute(sql,val)
#
# conn.commit()
#
# print(cursor.rowcount," record inserted")
# cursor.close()

# ########### 3.2
# cursor = conn.cursor()
#
# sql="insert into student (code,name,age) values (%s,%s,%s)"
#
# val=[
#     ("sv08","Trần Quyết Chiến",19),
#     ("sv09","Hồ Thắng",22),
#     ("sv10","Hoàng Hà",25),
#      ]
#
# cursor.executemany(sql,val)
#
# conn.commit()
#
# print(cursor.rowcount," record inserted")
# cursor.close()

# ######### 4.1
# cursor = conn.cursor()
# sql="update student set name='Hoàng Lão Tà' where Code='sv09'"
# cursor.execute(sql)
#
# conn.commit()
# print(cursor.rowcount," record(s) affected")

############ 4.2
# cursor = conn.cursor()
# sql="update student set name=%s where Code=%s"
# val=('Hoàng Lão Tà','sv09')
#
# cursor.execute(sql,val)
#
# conn.commit()
# print(cursor.rowcount," record(s) affected")

############ 5.1
conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)
cursor = conn.cursor()
sql="DELETE from student where ID=10"
cursor.execute(sql)

conn.commit()
print(cursor.rowcount," record(s) affected")

# ############ 5.2
# conn = mysql.connector.connect(
#                 host=server,
#                 port=port,
#                 database=database,
#                 user=username,
#                 password=password)
# cursor = conn.cursor()
# sql = "DELETE from student where ID=%s"
# val = (13,)
#
# cursor.execute(sql, val)
#
# conn.commit()
# print(cursor.rowcount," record(s) affected")