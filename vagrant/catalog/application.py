#
# This is the main part of the program to run Favorite Venue Application.
#
import random, string
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Sports, Arenas
from werkzeug.utils import secure_filename
#from oauth2client.client import flow_from_clientsecrets
#from oauth2client.client import FlowExchangeError

import json, requests, httplib2

#Creating upload folder for images and allowed extensions
#UPLOAD_FOLDER = ''
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

#Client Secrets file
#client_id = json.loads()

# Creates Session to the sportsvenue database
engine = create_engine('postgresql://sports:sports@localhost/sportsvenue')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#Shows the main page of the Venue Application
@app.route('/')
def showMainPage():
    return redirect(url_for('show_venues'))

#Creates JSON Endpoint
@app.route('/venuefinder/JSON')
def arenasJSON(arenas_id):
    venues = session.query('Arenas').all()
    venuesJSON = jsonify(Arenas = [Arenas.serialize \
    for venue in venues])
    return venuesJSON



#Shows all the sports venues
@app.route('/venuefinder/')
def show_venues():
    """Shows all the favorite venues in database
    """
    venues = session.query(Arenas).all
    return render_template('venue.html',venues=venues)

#Add New Venue to the Arenas Database
@app.route('/venuefinder/new', methods=['GET', 'POST'])
def NewVenue():
    print "NewVenue- Method"
    if request.method == 'POST':
        print "Post Request"
        newVenue = Arenas(name=request.form['name'], description=request.form['description'], url=request.form['url'])
        print newVenue
        session.add(newVenue)
        session.commit()
        flash("New Venue %s has been created" %(newVenue.name))
        return render_template('newVenue.html')
        #return redirect(url_for('show_venues'))
    else:
        user = login_session
        return render_template('newVenue.html')

# Edit Existing Venue Information
@app.route('/venuefinder/<int:arenas_id>/edit/', methods= ['GET', 'POST'])
def updateVenue(arenas_id):
    print "updatedvenue-method"
    updatevenues = session.query('Arenas').filter_by(id=arenas_id).one()
    if request.method == 'POST':
        if request.form['name']:
            flash("Updated Name successfully")
            updatevenues.name = request.form['name']
        if request.form['description']:
            flash ("Updated description successfully")
            updatedvenues.description = request.form['description']
        if request.form['url']:
            flash ("URL updated")
            updatevenues.url = request.form['url']
        # updateVenue = Arenas(name=request.form('name'), description=request.form('description'), image=request.form('venue_image'), url=request.form('url'))
        session.add(updatevenues)
        session.commit()
        flash("Arenas has been updated")
        return render_template('editVenue.html', venues = updatevenues)
    else:
        return render_template('editVenue.html')

#Delete Venue/Arenas Information
@app.route('/venuefinder/<int:arenas_id>/delete/', methods = ['GET', 'POST'])
def deleteVenue(arenas_id):
    venueToBeDeleted = session.query('Arenas').filter_by(id="arenas_id").one()
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
    return render_template('login.html', state=state)

@app.route('/logout')
def show_logout():
    return render_template('logout.html')

# def fbconnect()

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host= '0.0.0.0', port=5000)
