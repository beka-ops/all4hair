from flask import Flask, request

# View Services
def get_all_services(cursor):
    cursor.execute("SELECT * FROM services")
    return cursor.fetchall()

# Create Services
def create_services(cursor):
    sName = request.form['serviceName']
    price = request.form['listedPrice']
    sTime = request.form['howLong']
    cursor.execute("insert into services (serviceName, listedPrice, howLong) values (%s, %s, %s)",
                   (sName, price, sTime))
    return cursor.fetchall()

#Delete Services
def delete_services(cursor):
    cursor.execute("delete from services where service_id=%s", (request.form['service_id'],))
    return cursor.fetchall()

# Pull the Services
def pull_update_service(cursor):
    cursor.execute("select * from services where service_id=%s", (request.args.get('service_id'), ))
    return cursor.fetchall()

# Update Services
def update_services(cursor):
    cursor.execute("update services set serviceName=%s, listedPrice=%s, howLong=%s "
                   "where service_id=%s", (
                       request.form['serviceName'], request.form['listedPrice'], request.form['howLong'], request.form['service_id']))
    return cursor.fetchall()