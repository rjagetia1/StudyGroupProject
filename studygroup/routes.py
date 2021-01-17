# -------------------------------------------------------------------------------
# routes.py
# -------------------------------------------------------------------------------

from flask import render_template, request, make_response, redirect, url_for, session, send_from_directory, send_file

from studygroup import app, DEBUG
import studygroup.db as db

username = ''

#-----------------------------------------------------------------------

@app.route('/')
@app.route('/index')

def index():

    html = render_template('index.html')
    response = make_response(html)

    return response

#-----------------------------------------------------------------------

@app.route('/main', methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        if 'username' in request.form:
            username = request.form['username']
        else:
            username = None
        if "password" in request.form:
            password = request.form['password']
        else: 
            password = None
        if 'search' in request.form:
            search = request.form['search']
        else:
            search = None

        if 'title' in request.form:
            create_session = {}
            create_session['title'] = request.form['title']
            create_session['description'] = request.form['description']
            create_session['bio'] = request.form['bio']
            create_session['time'] = request.form['time']
            create_session['date'] = request.form['date']
            print(create_session['date'])
            create_session['max_parps'] = request.form['max_parps']
        
        html = render_template('main.html', username=username, password=password)
        
        response = make_response(html)

        return response
    if request.method == 'GET':
        username = request.args.get("username")
        password = request.args.get("password")
        if username != None:
            print(username)
        if password != None:
            print(password)
        
        html = render_template('main.html', username=username, password=password)
        
        response = make_response(html)
        
        return response


#-----------------------------------------------------------------------

@app.route('/my_workshops')
def my_workshops():

    html = render_template('my_workshops.html')
    response = make_response(html)

    return response
