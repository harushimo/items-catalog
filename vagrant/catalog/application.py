#
# This is the main part of the program to run Favorite Venue Application.
#
from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Sports, Arenas
import random, string
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.client import FlowExchangeError
from flask import make_response
import json, requests, httplib2

app = Flask(__name__)

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
def addNewVenue():
    if request.method == 'POST':
        newVenue = Arenas(name=request.form('name'), description=request.form('description'), image=request.form('venue_image'), url=request.form('url'))
        session.add(newVenue)
        session.commit()
        return redirect(url_for('show_venues'))
    else:
        return render_template('newVenue.html')

# Edit Existing Venue Information
@app.route('/venuefinder/<int:arenas.id>/update', methods= ['GET', 'POST'])
def updateVenue(arenas):
    if request.method == 'POST':
        newVenue = Arenas(name=request.form('name'), description=request.form('description'), image=request.form('venue_image'), url=request.form('url'))
        session.add(newVenue)
        session.commit()
        return redirect(url_for('show_venues'))
    else:
        return render_template('editVenue.html')




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
