#
# This is the main part of the program to run Favorite Venue Application.
#
import random, string
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Arenas
from werkzeug.utils import secure_filename
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import json, requests, httplib2

#Creating upload folder for images and allowed extensions
#UPLOAD_FOLDER = ''
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

#Client Secrets file
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Sports Venue Catalog'

# Creates Session to the sportsvenue database
engine = create_engine('postgresql://sports:sports@localhost/sportsvenue')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Login validator


#Shows the main page of the Venue Application
@app.route('/')
def showMainPage():
    return redirect(url_for('show_venues'))

#Creates JSON Endpoint
@app.route('/venuefinder/JSON')
def arenasJSON(arenas_id):
    arenas = session.query('Arenas').filter_by(id = "arenas_id").all()
    serializevenues = [i.serialize for i in arenas]
    return jsonify(serializevenues)



#Shows all the sports venues
@app.route('/venuefinder/', methods = ['GET', 'POST'])
def show_venues():
    """Shows all the favorite venues in database
    """
    venues = session.query(Arenas).all()
    print "GET Request"
    print venues
    return render_template('venue.html',venues=venues)

#show a single venue
# @app.route('/venuefinder/<int:arenas_id>')
# def showSingleVenue():
#     print "showSingleVenue - method"
#     singleVenue = session.query(Arenas).filter_by(id=arenas_id).one()
#     return



#Add New Venue to the Arenas Database
@app.route('/venuefinder/new', methods=['GET', 'POST'])
def NewVenue():
    print "NewVenue- Method"
    if request.method == 'POST':
        print "Post Request"
        newVenue = Arenas(name=request.form['name'], description=request.form['description'], url=request.form['url'])
        print newVenue.name, newVenue.description, newVenue.url
        session.add(newVenue)
        session.commit()
        flash("New Venue %s has been created" %(newVenue.name))
        print newVenue.name, newVenue.description, newVenue.url, newVenue.id
        return redirect(url_for('show_venues'))
    else:
        return render_template('newVenue.html')

# Edit Existing Venue Information
@app.route('/venuefinder/<int:arenas_id>/edit/', methods= ['GET', 'POST'])
def updateVenue(arenas_id):
    print "updatedvenue-method"
    print arenas_id
    updatevenues = session.query(Arenas).filter_by(id=arenas_id).first()
    if updatevenues:
        print "Inside updatevenues if statement"
        if request.method == 'POST':
            print "Inside request.method == post if statement"
            if request.form['name']:
                updatevenues.name = request.form['name']
                print updatevenues.name
                flash("Updated Name successfully")
            if request.form['description']:
                updatevenues.description = request.form['description']
                flash ("Updated description successfully")
                print updatevenues.description
            if request.form['url']:
                updatevenues.url = request.form['url']
                flash ("Updated URL")
                print updatevenues.url
            session.add(updatevenues)
            session.commit()
            flash("Arenas has been updated")
            #return redirect(url_for('show_venues'))
            return render_template('editVenue.html', venue = updatevenues)
        else:
            return render_template('editVenue.html')
    else:
        print "No venue"

#Delete Venue/Arenas Information
@app.route('/venuefinder/<int:arenas_id>/delete/', methods = ['GET', 'POST'])
def deleteVenue(arenas_id):
    print "deleteVenue - method"
    print arenas_id
    venueToBeDeleted = session.query(Arenas).filter_by(id=arenas_id).first()
    if request.method == 'POST':
        session.delete(venueToBeDeleted)
        flash("Arenas has be deleted")
        session.commit()
        return redirect(url_for('show_venues'))

#Login page
@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    print state
    return render_template('login.html', state=state)

#Google Login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        credentials = credentials.to_json()
        credentials = json.loads(credentials)
        # print credentials
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials['access_token']
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # print result

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials['id_token']['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials['access_token'], 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])

    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!<br> Email :'
    output += login_session['email']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;
                border-radius: 150px;-webkit-border-radius: 150px;
                -moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/logout')
def show_logout():
    return render_template('logout.html')

# def fbconnect()

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host= '0.0.0.0', port=5000)
