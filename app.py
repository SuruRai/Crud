from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import mysql.connector 
import logging

conn=mysql.connector.connect(user='Suruchi',password='12345678',host='database-1.caomyyms75ok.us-east-1.rds.amazonaws.com',database='crudapplication')
cursor=conn.cursor()
cursor.execute("DROP TABLE IF EXISTs students")
sql='''CREATE TABLE students(id INT(11) NOT NULL,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(255) NOT NULL)'''

cursor.execute(sql)
conn.close()

app = Flask(__name__)
logging.basicConfig(filename='my-logs', level=logging.INFO,format='%(levelname)s:%(message)s')
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'database-1.caomyyms75ok.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'Suruchi'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'crudapplication'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students=data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        logging.info(name)
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE students SET name=%s, email=%s, phone=%s
        WHERE id=%s
        """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=80)
