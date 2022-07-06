import MySQLdb
from flask import Flask, flash, render_template,request,redirect, url_for
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'OSM'
mysql = MySQL(app)

@app.route('/')
def index():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM teacher")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html',computers=data)

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return "Login via the login Form"
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        subject = request.form['subject']
        email = request.form['email']
        pswd = request.form['pswd']
        confirmpswd = request.form['condfirmpswd']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO teacher VALUES(%s,%s,%s,%s,%s)''',(id,name,subject,email,pswd))
        mysql.connection.commit()
        flash("Teacher Added Successfully")
        return redirect(url_for('index'))


@app.route('/update', methods=["POST"])
def update():
    id = request.form['id']
    name = request.form['name']
    subject = request.form['subject']
    email = request.form['email']
    pswd = request.form['pswd']
    print(id,name,subject,email,pswd)
    cursor = mysql.connection.cursor()
    cursor.execute("""UPDATE teacher SET name=%s, subject=%s, email=%s, pswd=%s WHERE id=%s""",(name,subject,email,pswd,id))
    mysql.connection.commit()
    flash("Teacher updated Successfully")
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def deete(id):
    # id = request.form['id']
    cursor = mysql.connection.cursor()
    cursor.execute("""DELETE FROM teacher where id=%s""",(id))
    mysql.connection.commit()
    flash("Teacher Deleted Successfully")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)