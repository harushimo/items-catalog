#
# This is the main part of the program to run Favorite Venue Application.
#
from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Sports, Arenas

app = Flask(__name__)

#Creates Database
engine = create_engine('sqlite://sportsvenue.db')
Base.metadata.create_all()

# Creates Session to the sportsvenue database
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Shows all the sports venues
@app.route('/')
@app.route('/venuefinder/')
def show_venues():
    """Shows all the favorite venues in database
    """
    # venues = session.query(Arenas).all
    # items = session.query().order_by(desc())
    # session.close()
    return render_template('default.html')

@app.route('/login')
def show_login():
    return render_template('login.html')


if __name__ = '__main__':
    app.debug = True
    app.run(host= '0.0.0.0', port=5000)
