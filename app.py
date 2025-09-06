import psycopg2
from flask import Flask, render_template, request,redirect,url_for

app = Flask(__name__)

def db_connect():
    conn = psycopg2.connect(database="interndb", user="postgres", password="1234", host="localhost", port="5432")
    return conn

@app.route('/')
def index():
    conn=db_connect()
    cur=conn.cursor()
    cur.execute('''SELECT * FROM students ORDER BY id''')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", data=data)

@app.route('/create', methods=['POST'])
def create():
    conn=db_connect()
    cur=conn.cursor()
    name=request.form['name']
    email=request.form['email']
    age=request.form['age']
    course=request.form['course']

    cur.execute('''INSERT INTO students(name,email,age,course,created_at) VALUES(%s,%s,%s,%s,NOW())''',(name,email,age,course))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    conn=db_connect()
    cur=conn.cursor()

    name=request.form['name']
    email=request.form['email']
    age=request.form['age']
    course=request.form['course']
    id=request.form['id']

    cur.execute('''UPDATE students SET name=%s,email=%s,age=%s,course=%s WHERE id=%s''',(name,email,age,course,id))
    conn.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    conn=db_connect()
    cur=conn.cursor()
    id=request.form['id']
    cur.execute('''DELETE FROM students WHERE id=%s''',(id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

