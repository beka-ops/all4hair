from flask import Flask, redirect, render_template, request, url_for, session
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="mysql.railway.internal",
    port=3306,
    user="root",
    password="IZvzxNoSLdklFQnVjANxvxClFxRENfcO",
    database="railway"
)

def get_cursor():
    db.reconnect()
    return db.cursor()

@app.route('/')
def home():
    return redirect(url_for('view_customer'))

@app.route('/c_register', methods=['GET', 'POST'])
def c_register():
    if request.method == 'POST':
        fname_data = request.form['firstName']
        lname_data = request.form['lastName']
        email_data = request.form['emailAddress']
        number_data = request.form['phoneNumber']
        cursor = get_cursor()
        cursor.execute("insert into customer (firstName, lastName,emailAddress, phoneNumber) values (%s, %s, %s, %s)", (fname_data,lname_data,email_data,number_data ))
        db.commit()
        return redirect(url_for('view_customer'))
    elif request.method == 'GET':
        return render_template('c_register.html')

@app.route('/view_customer', methods=['GET', 'POST'])
def view_customer():
    if request.method == 'GET':
        cursor = get_cursor()
        cursor.execute("select * from customer")
        results = cursor.fetchall()
        return render_template('customers.html', customers=results)
    elif request.method == 'POST':
        return redirect(url_for('delete_customer'), url_for('c_modify'))

@app.route('/delete_customer', methods=['GET', 'POST'])
def delete_customer():
    if request.method == 'POST':
        cursor = get_cursor()
        cursor.execute("delete from customer where customer_id=%s", (request.form['customer_id'], ))
        db.commit()
        results = cursor.fetchall()
        return redirect(url_for('view_customer'))

@app.route('/c_modify', methods=['GET', 'POST'])
def c_modify():
    if request.method == 'GET':
        cursor = get_cursor()
        cursor.execute("select * from customer where customer_id=%s", (request.args.get('customer_id'), ))
        return render_template('c_edit.html', customer=cursor.fetchall())
    elif request.method == 'POST':
        cursor = get_cursor()
        cursor.execute("update customer set firstName=%s, lastName=%s, emailAddress=%s, phoneNumber=%s "
                       "where customer_id=%s", (request.form['firstName'], request.form['lastName'], request.form['emailAddress'] , request.form['phoneNumber'] ,request.form['customer_id']))
        db.commit()
        return redirect(url_for('view_customer'))

if __name__ == '__main__':
    app.run(debug=True)