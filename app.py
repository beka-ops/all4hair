from flask import Flask, redirect, render_template, request, url_for, session
from routes.customer import get_all_customers, delete_customers, create_customer, update_customer, pull_update_customer, get_customer_favorites, get_customer_bookings
from routes.service import get_all_services, create_services, delete_services, pull_update_service, update_services
from routes.provider import get_all_providers, delete_provider, create_provider, pull_update_provider, update_provider, pull_update_location
from routes.provider_has_services import (get_all_providers_assign, get_all_services_assign, add_provider_has_services, listing,
                                          add_favorite_ps, create_booking, view_appt, update_booking, pull_update_booking, payment_history)
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
"""

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="d7?NV8',6K3M",
    database="all4hair"
)
"""

def get_cursor():
    db.reconnect()
    return db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/c_register', methods=['GET', 'POST'])
def c_register():
    if request.method == 'POST':
        try:
            cursor = get_cursor()
            results = create_customer(cursor)
            db.commit()
            return redirect(url_for('view_customer'))
        except errors.IntegrityError:
            return render_template('c_register.html', error="The email has been entered before, please try again.")
    elif request.method == 'GET':
        return render_template('c_register.html')

@app.route('/view_customer', methods=['GET'])
def view_customer():
    cursor = get_cursor()
    results = get_all_customers(cursor)
    return render_template('customers.html', customers=results, error=None)

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    try:
        cursor = get_cursor()
        results = delete_customers(cursor)
        db.commit()
        return redirect(url_for('view_customer'))
    except errors.IntegrityError:
        cursor = get_cursor()
        results = get_all_customers(cursor)
        return render_template('customers.html', customers=results, error="This customer information is in use, so it cannot be deleted.")

@app.route('/c_modify', methods=['GET', 'POST'])
def c_modify():
    if request.method == 'GET':
        customer_id = request.args.get('customer_id')
        cursor = get_cursor()
        results = pull_update_customer(cursor)
        favorites = get_customer_favorites(cursor, customer_id)
        bookings = get_customer_bookings(cursor, customer_id)
        return render_template('c_edit.html', customer=results, favorites=favorites, bookings=bookings, error=None)
    elif request.method == 'POST':
        try:
            cursor = get_cursor()
            update_customer(cursor)
            db.commit()
            return redirect(url_for('view_customer'))
        except errors.IntegrityError:
            customer_id = request.args.get('customer_id')
            cursor = get_cursor()
            results = pull_update_customer(cursor)
            favorites = get_customer_favorites(cursor, customer_id)
            bookings = get_customer_bookings(cursor, customer_id)
            return render_template('c_edit.html', customer=results, favorites=favorites, bookings=bookings, error="Email has been used before. Try another email.")


# Routing services

@app.route('/view_services', methods=['GET'])
def view_services():
    cursor = get_cursor()
    results = get_all_services(cursor)
    return render_template('services.html', services = results, error=None)

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
    try:
        cursor = get_cursor()
        results = delete_services(cursor)
        db.commit()
        return redirect(url_for('view_services'))
    except errors.IntegrityError:
        cursor = get_cursor()
        results = get_all_services(cursor)
        return render_template('services.html', services = results, error="This service is in use, so it cannot be deleted.")


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
        return render_template('providers.html', providers=results, error=None)

@app.route('/delete_provider', methods=['POST'])
def delete_providers():
    try:
        cursor = get_cursor()
        delete_provider(cursor)
        db.commit()
        return redirect(url_for('view_providers'))
    except errors.IntegrityError:
        cursor = get_cursor()
        results = get_all_providers(cursor)
        return render_template('providers.html', providers=results, error="This provider information is in use, so it cannot be deleted.")

@app.route('/p_register', methods=['GET', 'POST'])
def register_provider():
    if request.method == 'POST':
        try:
            cursor = get_cursor()
            create_provider(cursor)
            db.commit()
            return redirect(url_for('view_providers'))
        except errors.IntegrityError:
            return render_template('p_register.html', error="The email has been entered before, please try again.")
    elif request.method == 'GET':
        return render_template('p_register.html', error=None)

@app.route('/p_modify', methods=['GET', 'POST'])
def p_modify():
    if request.method == 'GET':
        cursor = get_cursor()
        results = pull_update_provider(cursor)
        res_loc = pull_update_location(cursor)
        return render_template('p_edit.html', provider=results, location=res_loc, error=None)
    elif request.method == 'POST':
        try:
            cursor = get_cursor()
            update_provider(cursor)
            db.commit()
            return redirect(url_for('view_providers'))
        except errors.IntegrityError:
            cursor = get_cursor()
            results = pull_update_provider(cursor)
            res_loc = pull_update_location(cursor)
            return render_template('p_edit.html', provider=results, location=res_loc, error="Make sure you are using a unique email address.")


@app.route('/assign_services', methods=['GET', 'POST'])
def assign_services():
    if request.method == 'GET':
        cursor = get_cursor()
        result_1 = get_all_providers_assign(cursor)
        result_2 = get_all_services_assign(cursor)
        return render_template('assign_service.html', providers=result_1, services=result_2, error=None)
    elif request.method == 'POST':
        try:
            cursor = get_cursor()
            add_provider_has_services(cursor)
            db.commit()
            return redirect(url_for('assign_services'))
        except errors.IntegrityError:
            cursor = get_cursor()
            result_1 = get_all_providers_assign(cursor)
            result_2 = get_all_services_assign(cursor)
            return render_template('assign_service.html', providers=result_1, services=result_2, error="The Provider already provides this service. Please pick a new service.")

@app.route('/listing', methods=['GET', 'POST'])
def provider_service_listing():
    if request.method == 'GET':
        cursor = get_cursor()
        results = listing(cursor)
        result_cust = get_all_customers(cursor)
        return render_template('psl_view.html', psl=results, customers=result_cust, error=None)

@app.route('/add_favs', methods=['POST'])
def add_favor():
    try:
        cursor = get_cursor()
        result = add_favorite_ps(cursor)
        db.commit()
        return redirect(url_for('provider_service_listing'))
    except errors.IntegrityError:
        cursor = get_cursor()
        results = listing(cursor)
        result_cust = get_all_customers(cursor)
        return render_template('psl_view.html', psl=results, customers=result_cust, error="Customer has already liked <3 this provider! Pick another one ;)")

@app.route('/booking', methods=['GET', 'POST'])
def add_booking():
    if request.method == 'GET':
        provider_info = request.args.get('provider_id')
        service_info = request.args.get('service_id')
        location_info = request.args.get('location_id')
        customer_info = request.args.get('customer_id')
        return render_template('appt.html', provider_id=provider_info, service_id=service_info, location_id=location_info, customer_id=customer_info)
    elif request.method == 'POST':
        cursor = get_cursor()
        result = create_booking(cursor)
        db.commit()
        return redirect(url_for('provider_service_listing'))

@app.route('/view_booking', methods=['GET', 'POST'])
def view_booking():
    if request.method == 'GET':
        cursor = get_cursor()
        result = view_appt(cursor)
        return render_template('bookings.html', booking=result)

@app.route('/b_modify', methods=['GET', 'POST'])
def b_modify():
    if request.method == 'GET':
        booking_info = request.args.get('booking_id')
        cursor = get_cursor()
        booking = pull_update_booking(cursor, booking_info)
        return render_template('b_edit.html',booking=booking)
    elif request.method == 'POST':
        cursor = get_cursor()
        update_booking(cursor)
        db.commit()
        return redirect(url_for('view_booking'))

@app.route('/paid', methods=['GET'])
def view_pay_hist():
    cursor = get_cursor()
    results = payment_history(cursor)
    return render_template('payment_history.html', pay_history = results)

@app.route('/reports', methods=['GET'])
def cust_reports():
    cursor = get_cursor()
    cursor.execute("select concat(c.firstName, ' ', c.lastName) as 'Name', count(b.booking_id) as 'Total Booking' from booking b join customer c on b.customer_id=c.customer_id where b.status!='CANCELLED' group by c.customer_id")
    customer_report = cursor.fetchall()
    cursor.execute("select concat(p.firstName, ' ', p.lastName) as 'Name', sum(case when ph.payment_status = 'COMPLETED' then ph.paid_price else 0.00 end) as 'Total Revenue', 	count(case when b.booking_date > now() then b.booking_id else null end) as 'Future Booking' from providers p  left join booking b on b.provider_id=p.provider_id left join payment_history ph on ph.booking_id=b.booking_id group by p.provider_id")
    provider_report = cursor.fetchall()
    return render_template('reports.html', customer_report=customer_report, provider_report=provider_report)


if __name__ == '__main__':
    app.run(debug=True)