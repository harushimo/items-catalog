#
# This is the main part of the program to run Favorite Venue Application.
#
import random, string
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import make_response
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Sports, Arenas
#from oauth2client.client import flow_from_clientsecrets
#from oauth2client.client import FlowExchangeError

import json, requests, httplib2

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

#Shows all the sports venues
@app.route('/venuefinder/')
def show_venues():
    """Shows all the favorite venues in database
    """
    venues = session.query(Arenas).all
    return render_template('default.html',venues=venues)

#Add New Venue to the Arenas Database
@app.route('/venuefinder/new', methods=['GET', 'POST'])
def NewVenue():
    print "NewVenue- Method"
    if request.method == 'POST':
        newVenue = Arenas(name=request.form('name'), description=request.form('description'), image=request.form('venue_image'), url=request.form('url'))
        print newVenue
        session.add(newVenue)
        session.commit()
        flash("New Venue %s has been created" %(newVenue.name))
        return redirect(url_for('show_venues'))
    else:
        user = login_session
        return render_template('newVenue.html')

# Edit Existing Venue Information
@app.route('/venuefinder/<int:arenas_id>/update', methods= ['GET', 'POST'])
def updateVenue(arenas):
    updatevenues = session.query('Arenas').filter_by(id="arenas_id").one()
    if request.method == 'POST':
        if request.form == 'name':
            updatevenues.name = request.form('name')
        if request.form == 'description':
            updatedvenues.description = request.form('description')
        if request.form == 'image':
            updatevenues.image = request.form('image')
        if request.form == 'url':
            updatevenues.url = request.form('url')
        # updateVenue = Arenas(name=request.form('name'), description=request.form('description'), image=request.form('venue_image'), url=request.form('url'))
        session.add(updatevenues)
        session.commit()
        flash("Arenas has been updated")
        return redirect(url_for('show_venues'))
    else:
        return render_template('editVenue.html')

#Delete Venue/Arenas Information
@app.route('/venuefinder/<int:arenas_id>/delete', methods = ['GET', 'POST'])
def deleteVenue(arenas):
    venueToBeDeleted = session.query('Arenas').filter_by(id="arenas_id").one()
    if request.method == 'POST':
        session.delete(venueToBeDeleted)
        flash("Arenas has be deleted")
        session.commit()
        return redirect(url_for('show_venues'))

#Login information to Google and Facebook
@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/logout')
def show_logout():
    return render_template('logout.html')

# def fbconnect()

if __name__ == '__main__':
    app.debug = True
    app.run(host= '0.0.0.0', port=5000)
