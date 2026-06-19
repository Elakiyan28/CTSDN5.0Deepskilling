import mysql.connector

# Connect to MySQL Server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Se2809!.@sairam",   
    database="college_db"
)

cursor = conn.cursor()

# 1. Insert a new student
insert_query = """
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year)
VALUES (%s, %s, %s, %s, %s, %s)
"""
student_data = ("Suresh", "K", "suresh.k@example.com", "2005-06-15", 1, 2023)
cursor.execute(insert_query, student_data)
conn.commit()
print("Inserted student:", cursor.rowcount)

# 2. Update a student’s grade in enrollments
update_query = "UPDATE enrollments SET grade = %s WHERE student_id = %s AND course_id = %s"
cursor.execute(update_query, ("A+", 1, 1))
conn.commit()
print("Updated grade:", cursor.rowcount)

# 3. Select students with their department
select_query = """
SELECT s.first_name, s.last_name, d.dept_name
FROM students s
INNER JOIN departments d ON s.department_id = d.dept_id
"""
cursor.execute(select_query)
for row in cursor.fetchall():
    print(row)

# Close connection
cursor.close()
conn.close()
