from operator import concat

from flask import request

def get_all_providers_assign(cursor):
    cursor.execute("SELECT * FROM providers")
    return cursor.fetchall()

def get_all_services_assign(cursor):
    cursor.execute("SELECT * FROM services")
    return cursor.fetchall()

def add_provider_has_services(cursor):
    provider_info = request.form['provider_drop']
    service_info = request.form['service_drop']
    cursor.execute("insert into provider_has_service (provider_id, service_id) values (%s, %s)",
                   (provider_info, service_info))
    return cursor.fetchall()

def listing(cursor):
    cursor.execute("select * from provider_service_listing")
    return cursor.fetchall()

# Favorite
def add_favorite_ps(cursor):
    cursor.execute("insert into favorites (customer_id, provider_id, service_id) values (%s, %s, %s)",
                   (request.form['customer_id'], request.form['provider_id'], request.form['service_id']))
    return cursor.fetchall()

# Booking
def create_booking(cursor):
    booking_datetime = request.form['book_date'] + ' ' + request.form['book_time']
    cursor.execute("insert into booking (booking_date, status, customer_id, provider_id, service_id, location_id) values (%s, %s, %s, %s, %s, %s)",
                   (booking_datetime, 'PENDING', request.form['customer_id'], request.form['provider_id'], request.form['service_id'], request.form['location_id']))
    return cursor.fetchall()

# View Booking
def view_appt(cursor):
    cursor.execute("select * from booked_appointments")
    return cursor.fetchall()

def pull_update_booking(cursor, booking_id):
    cursor.execute("select * from booking where booking_id=%s", (booking_id,))
    return cursor.fetchall()

def update_booking(cursor):
    cursor.execute("update booking set booking_date=%s, status=%s where booking_id=%s", (request.form['book_date'], request.form['b_status'], request.form['booking_id']))
    return cursor.fetchall()