#
# from retail_project.connectors.employee_connector import EmployeeConnector
#
# ec=EmployeeConnector()
# ec.connect()
# em=ec.login("putin@gmail.com", "123")
# if em==None:
#     print("Login Failed")
# else:
#     print("Login Succeeded")
#     print(em)
#
# #test get all employee
# print("List of Employee")
# ds = ec.get_all_employee()
# print(ds)
# for emp in ds:
#     print(emp)

from retail_project.connectors.employee_connector import EmployeeConnector

ec=EmployeeConnector()
ec.connect()
em=ec.login("putin@gmail.com", "123")
if em==None:
    print("Login Failed")
else:
    print("Login Succeeded")
    print(em)


#test get_all_employee:
print('List of Employee:')
ds=ec.get_all_employee()
print(ds)
for emp in ds:
    print(emp)

id = 3
emp = ec.get_detail_infor(id)
if emp == None:
    print("Không có nhân viên nào cso mã = ", id)
else:
    print("Tìm thấy nhân viên có mã =", id)