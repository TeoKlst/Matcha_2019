import sqlite3
from employee import Employee

# Connection object that represents the database
# conn = sqlite3.connect('employee.db')
# Creates fresh new database everytime in RAM
conn = sqlite3.connect(':memory:')

# Cursor allows us to execute sql commands
cur = conn.cursor()

# Dock string, a string that can be written in multiple lines without any special breaks
cur.execute("""CREATE TABLE employees (
            first TEXT,
            last TEXT,
            pay INTEGER
            )""")

# Inserts employee
# Commit after every insert, update or delete.
# But with context manager we can manage a setup and teardown of resources automatically.
# With Sqlite connection objects can be used context managers that automatically commit or rollback transactions.
# No need for commit statement
def insert_emp(emp):
    with conn:
        cur.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

def get_emps_by_name(lastname):
    cur.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
    return cur.fetchall()

def update_pay(emp, pay):
    with conn:
        cur.execute("""UPDATE employees SET pay=:pay
                    WHERE first=:first AND last=:last""",
                    {'first': emp.first, 'last': emp.last, 'pay': pay})

def remove_emp(emp):
    with conn:
        cur.execute("DELETE from employees WHERE first=:first AND last=:last",
                    {'first': emp.first, 'last': emp.last})

emp_1 = Employee('John', 'Doe', 20000)
emp_2 = Employee('Jane', 'Doe', 25000)

insert_emp(emp_1)
insert_emp(emp_2)

emps = get_emps_by_name('Doe')
print(emps)

update_pay(emp_2, 95000)
remove_emp(emp_1)

emps = get_emps_by_name('Doe')
print(emps)

conn.close()



# <----                                Falls under employee creation                                ---->

# Incorrect method of formating, susceptible to sql injection
# cur.execute("INSERT INTO employees VALUES ('{}', '{}', {})".format(emp_1.first, emp_1.last, emp_1.pay))

# Passing a tuple of all values
# cur.execute("INSERT INTO employees VALUES (?, ?, ?)", (emp_1.first, emp_1.last, emp_1.pay))
# conn.commit()

# # Correct way, passing a dictionary, the keys fill in the placeholders
# cur.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp_2.first, 'last': emp_2.last, 'pay': emp_2.pay})
# conn.commit()

# cur.execute("INSERT INTO employees VALUES ('John', 'Kelestura', 60000)")
# conn.commit()

# cur.execute("SELECT * FROM employees WHERE last='Kelestura'")
# # Question mark approach requires a tuple, and the comma is needed otherwise error
# cur.execute("SELECT * FROM employees WHERE last=?", ('Kelestura',))
# print(cur.fetchall())

# cur.execute("SELECT * FROM employees WHERE last=:last", {'last':'Doe'})
# print(cur.fetchall())

# # Commits current transaction
# conn.commit()
