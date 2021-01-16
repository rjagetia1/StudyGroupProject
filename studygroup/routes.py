# -------------------------------------------------------------------------------
# routes.py
# -------------------------------------------------------------------------------

from flask import render_template, request, make_response, redirect, url_for, session, send_from_directory, send_file

from studygroup import app, DEBUG
import studygroup.db as db

#-----------------------------------------------------------------------

@app.route('/')
@app.route('/index')

def index():
    
    html = render_template('index.html')
    response = make_response(html)

    return response

#-----------------------------------------------------------------------

@app.route('/main')
def main():

    html = render_template('main.html')
    response = make_response(html)

    return response


#-----------------------------------------------------------------------

@app.route('/my_workshops')
def my_workshops():

    html = render_template('my_workshops.html')
    response = make_response(html)

    return response
