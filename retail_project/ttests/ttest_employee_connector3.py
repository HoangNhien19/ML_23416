from retail_project.connectors.employee_connector import EmployeeConnector
from retail_project.models.employee import Employee

ec=EmployeeConnector()
ec.connect()
emp=Employee()
emp.ID = 9
emp.EmployeeCode = "EMP888"
emp.Name="HAHA"
emp.Phone ="0294858493"
emp.Email="dora@gmail.com"
emp.Password="234"
emp.IsDeleted=0

result = ec.update_one_employee(emp)
if result > 0:
    print("Chúc mừng nha, đã thêm thành công")
else:
    print("That bai")