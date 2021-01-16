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
            title = request.form['title']
        else:
            title = None
        if 'description' in request.form:
            description = request.form['description']
        else:
            description = None
        if 'bio' in request.form:
            bio = request.form['bio']
        else:
            bio = None
        if 'time' in request.form:
            time = request.form['time']
        else:
            time = None
        if 'date' in request.form:
            date = request.form['date']
        else:
            date = None
        if 'max_parps' in request.form:
            max_parps = request.form['max_parps']
        else:
            max_parps = None
        
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
