from absl.logging import exception
from flask import Flask, redirect, render_template, request, url_for, session
from routes.customer import get_all_customers, delete_customers, create_customer, update_customer, pull_update_customer
from routes.service import get_all_services, create_services, delete_services, pull_update_service, update_services
from routes.provider import get_all_providers, delete_provider, create_provider, pull_update_provider, update_provider, pull_update_location
import mysql.connector
from mysql.connector import errors

app = Flask(__name__)


db = mysql.connector.connect(
    host="mysql.railway.internal",
    port=3306,
    user="root",
    password="IZvzxNoSLdklFQnVjANxvxClFxRENfcO",
    database="railway"
)
""""
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="d7?NV8',6K3M",
    database="all4hair"
)"""

def get_cursor():
    db.reconnect()
    return db.cursor()

@app.route('/')
def home():
    return redirect(url_for('view_providers'))

@app.route('/c_register', methods=['GET', 'POST'])
def c_register():
    if request.method == 'POST':
        try:
            cursor = get_cursor()
            results = create_customer(cursor)
            db.commit()
            return redirect(url_for('view_customer'))
        except errors.IntegrityError:
            return render_template('c_register.html', error="The email has been entered before, please try again later.")
    elif request.method == 'GET':
        return render_template('c_register.html')

@app.route('/view_customer', methods=['GET'])
def view_customer():
    cursor = get_cursor()
    results = get_all_customers(cursor)
    return render_template('customers.html', customers=results)

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    cursor = get_cursor()
    results = delete_customers(cursor)
    db.commit()
    return redirect(url_for('view_customer'))

@app.route('/c_modify', methods=['GET', 'POST'])
def c_modify():
    if request.method == 'GET':
        cursor = get_cursor()
        results = pull_update_customer(cursor)
        return render_template('c_edit.html', customer=results)
    elif request.method == 'POST':
        cursor = get_cursor()
        update_customer(cursor)
        db.commit()
        return redirect(url_for('view_customer'))

# Routing services

@app.route('/view_services', methods=['GET'])
def view_services():
    cursor = get_cursor()
    results = get_all_services(cursor)
    return render_template('services.html', services = results)

@app.route('/s_register', methods=['GET', 'POST'])
def register_service():
    if request.method == 'POST':
        cursor = get_cursor()
        results = create_services(cursor)
        db.commit()
        return redirect(url_for('view_services'))

    elif request.method == 'GET':
        return render_template('s_register.html')


@app.route('/delete_service', methods=['POST'])
def delete_service():
    cursor = get_cursor()
    results = delete_services(cursor)
    db.commit()
    return redirect(url_for('view_services'))


@app.route('/s_modify', methods=['GET', 'POST'])
def s_modify():
    if request.method == 'GET':
        cursor = get_cursor()
        result = pull_update_service(cursor)
        return render_template('s_edit.html', services = result)
    elif request.method == 'POST':
        cursor = get_cursor()
        update_services(cursor)
        db.commit()
        return redirect(url_for('view_services'))


# Route Providers
@app.route('/view_providers', methods=['GET'])
def view_providers():
    if request.method == 'GET':
        cursor = get_cursor()
        results = get_all_providers(cursor)
        return render_template('providers.html', providers=results)

@app.route('/delete_provider', methods=['POST'])
def delete_providers():
    if request.method == 'POST':
        cursor = get_cursor()
        delete_provider(cursor)
        db.commit()
        return redirect(url_for('view_providers'))

@app.route('/p_register', methods=['GET', 'POST'])
def register_provider():
    if request.method == 'POST':
        cursor = get_cursor()
        create_provider(cursor)
        db.commit()
        return redirect(url_for('view_providers'))
    elif request.method == 'GET':
        return render_template('p_register.html')

@app.route('/p_modify', methods=['GET', 'POST'])
def p_modify():
    if request.method == 'GET':
        cursor = get_cursor()
        results = pull_update_provider(cursor)
        res_loc = pull_update_location(cursor)
        return render_template('p_edit.html', provider=results, location=res_loc)
    elif request.method == 'POST':
        cursor = get_cursor()
        update_provider(cursor)
        db.commit()
        return redirect(url_for('view_providers'))


if __name__ == '__main__':
    app.run(debug=True)