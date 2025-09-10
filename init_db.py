import psycopg2

conn=psycopg2.connect(database="interndb", user="postgres", password="1234", host="localhost", port="5432")
cur=conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS students (id SERIAL PRIMARY KEY,name Varchar(100),email Varchar(100),age integer,course Varchar(100),created_at Varchar(100));''')
cur.execute('''INSERT INTO students (name,email,age,course,created_at) VALUES ('om','om@gmail.com',20,'python',now());''')
conn.commit()
cur.close()
conn.close()
