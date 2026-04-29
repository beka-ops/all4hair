from flask import Flask, request


# View Customers
def get_all_customers(cursor):
    cursor.execute("SELECT * FROM customer")
    return cursor.fetchall()

# Delete Certain Customers
def delete_customers(cursor):
    cursor.execute("delete from customer where customer_id=%s", (request.form['customer_id'], ))
    return cursor.fetchall()

# Sign Up a Customer
def create_customer(cursor):
    fname_data = request.form['firstName']
    lname_data = request.form['lastName']
    email_data = request.form['emailAddress']
    number_data = request.form['phoneNumber']
    cursor.execute("insert into customer (firstName, lastName,emailAddress, phoneNumber) values (%s, %s, %s, %s)",
                   (fname_data, lname_data, email_data, number_data))
    return cursor.fetchall()

def pull_update_customer(cursor):
    cursor.execute("select * from customer where customer_id=%s", (request.args.get('customer_id'), ))
    return cursor.fetchall()

# Update Customer Information
def update_customer(cursor):
    cursor.execute("update customer set firstName=%s, lastName=%s, emailAddress=%s, phoneNumber=%s "
                   "where customer_id=%s", (
                   request.form['firstName'], request.form['lastName'], request.form['emailAddress'],
                   request.form['phoneNumber'], request.form['customer_id']))
    return cursor.fetchall()

def get_customer_favorites(cursor, customer_id):
    cursor.callproc('favorite_provider', [customer_id])
    for result in cursor.stored_results():
        return result.fetchall()

def get_customer_bookings(cursor, customer_id):
    cursor.callproc('booking_per_customer', [customer_id])
    for result in cursor.stored_results():
        return result.fetchall()