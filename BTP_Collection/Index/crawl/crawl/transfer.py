import mysql.connector as mysql
from mysql.connector import Error

try:
    thread = mysql.connect(host='localhost',
                                user='mesh_admin',
                                password='i@am@great@no',
                                database='mesh_visited')
except Error as e:
    raise Exception("Error while connecting to MySQL database ", e)
print("Connected!")
batch = 1
cursor = thread.cursor()
"""
query = "INSERT INTO visited_urls (urls, status) VALUES (%s, %s)"
values = []
file = open('visited_urls/visited_1.txt')
line = file.readline().rstrip('\n')
i = 1
j = 0
while line != '':
    if i%batch == 0:
        cursor.executemany(query, values)
        thread.commit()
        values.clear()
        j += 1
        print('Batch '+str(j) + ' added.')
    line = file.readline().rstrip('\n')
    values.append((line, True))
    i += 1
"""
values = ('hhh',)
query = "SELECT status FROM visited_urls WHERE urls = %s"
cursor.execute(query, values)
print(cursor.fetchall())
print("Closed!")
