from flask import  request

# View Providers
def get_all_providers(cursor):
    cursor.execute("SELECT * FROM providers")
    return cursor.fetchall()

# Delete Providers
def delete_provider(cursor):
    cursor.execute("select location_id from provider_has_location where provider_id=%s", (request.form['provider_id'],))
    location_id = cursor.fetchone()[0]
    cursor.execute("delete from provider_has_location where location_id=%s and provider_id=%s", (location_id, request.form['provider_id'],))
    cursor.execute("delete from providers where provider_id=%s", (request.form['provider_id'], ))
    cursor.execute("delete from location where location_id=%s", (location_id, ))
    return cursor.fetchall()

# Add Provider
def create_provider(cursor):
    cursor.execute("insert into providers (firstName, lastName, businessName, emailAddress, phoneNumber, providerStatus) values (%s, %s, %s, %s, %s, %s)",
                   (request.form['firstName'], request.form['lastName'], request.form['businessName'], request.form['emailAddress'],
                    request.form['phoneNumber'], request.form['pstatus']))
    provider_id = cursor.lastrowid
    cursor.execute("insert into location (streetName, city, state, zipCode) values (%s, %s, %s, %s)", (request.form['streetName'],
                  request.form['cityName'], request.form['stateName'], request.form['zipCode']))
    location_id = cursor.lastrowid
    cursor.execute("insert into provider_has_location (provider_id, location_id) values (%s, %s)",
                   (provider_id, location_id))
    return cursor.fetchall()


def pull_update_provider(cursor):
    cursor.execute("select * from providers where provider_id=%s", (request.args.get('provider_id'), ))
    provider_id = cursor.lastrowid
    return cursor.fetchall()


def pull_update_location(cursor):
    cursor.execute("select * "
                   "  from location as l join provider_has_location as pl on l.location_id=pl.location_id "
                   "  where pl.provider_id=%s", (request.args.get('provider_id'), ))
    location_id = cursor.lastrowid
    return cursor.fetchall()

# Update Customer Information
def update_provider(cursor):
    cursor.execute("update providers set firstName=%s, lastName=%s, businessName=%s, emailAddress=%s, phoneNumber=%s, providerStatus=%s "
                   "where provider_id=%s", (
                   request.form['firstName'], request.form['lastName'], request.form['businessName'], request.form['emailAddress'],
                   request.form['phoneNumber'], request.form['pstatus'], request.form['provider_id']))
    cursor.execute("update location set streetName=%s, city=%s, state=%s, zipCode=%s where location_id=%s", (request.form['streetName'],
                  request.form['cityName'], request.form['stateName'], request.form['zipCode'], request.form['location_id']))
    return cursor.fetchall()
