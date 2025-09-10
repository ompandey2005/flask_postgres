import psycopg2
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

def db_connect():
    return psycopg2.connect(database="interndb", user="postgres", password="1234", host="localhost", port="5432")

def build_query_and_params(args):
    course = args.get('course')
    age = args.get('age')
    sort = args.get('sort')
    order = (args.get('order') or 'asc').lower()

    allowed_sort_fields = {'age': 'age', 'created_at': 'created_at'}
    if order not in ('asc', 'desc'):
        order = 'asc'

    query = "SELECT id, name, email, age, course, created_at FROM students"
    filters = []
    params = []

    if course:
        filters.append("course ILIKE %s")
        params.append(course)

    if age:
        filters.append("age = %s")
        params.append(age)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    if sort in allowed_sort_fields:
        query += f" ORDER BY {allowed_sort_fields[sort]} {order.upper()}"
    else:
        query += " ORDER BY id"

    return query, params

@app.route('/')
def index():
    conn = db_connect()
    cur = conn.cursor()
    query, params = build_query_and_params(request.args)
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", data=data)


@app.route('/students', methods=['GET'])
def students_api():
    conn = db_connect()
    cur = conn.cursor()
    query, params = build_query_and_params(request.args)
    cur.execute(query, params)
    rows = cur.fetchall()
    # convert to list of dicts for JSON
    cols = [desc[0] for desc in cur.description]
    students = [dict(zip(cols, r)) for r in rows]
    cur.close()
    conn.close()
    return jsonify({'students': students, 'count': len(students)})

@app.route('/create', methods=['POST'])
def create():
    conn = db_connect()
    cur = conn.cursor()
    name = request.form['name']
    email = request.form['email']
    age = request.form.get('age') or None
    course = request.form.get('course') or None

    cur.execute("INSERT INTO students (name, email, age, course, created_at) VALUES (%s, %s, %s, %s, NOW())",(name, email, age, course))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    conn = db_connect()
    cur = conn.cursor()
    name = request.form['name']
    email = request.form['email']
    age = request.form.get('age') or None
    course = request.form.get('course') or None
    id = request.form['id']

    cur.execute("UPDATE students SET name=%s, email=%s, age=%s, course=%s WHERE id=%s",(name, email, age, course, id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    conn = db_connect()
    cur = conn.cursor()
    id = request.form['id']
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
