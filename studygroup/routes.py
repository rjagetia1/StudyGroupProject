# -------------------------------------------------------------------------------
# routes.py
# -------------------------------------------------------------------------------

from flask import render_template, request, make_response, redirect, url_for, session, send_from_directory, send_file

from studygroup import app, DEBUG, bcrypt
import studygroup.dbf as dbf

#-----------------------------------------------------------------------

@app.route('/')
@app.route('/index')

def index():
    session['username'] = None

    html = render_template('index.html')
    response = make_response(html)

    return response

#-----------------------------------------------------------------------

@app.route('/main', methods=["GET", "POST"])
def main():
    if session['username'] is None:
        redirect(url_for('index'))

    if request.method == 'POST':
        if 'username' in request.form:
            username = request.form['username']
            if "password" in request.form:
                password = request.form['password']
                # pw_hash = bcrypt.generate_password_hash(password)
                ret = dbf.login(username, password)
                if ret == -1:
                    html = render_template('index.html', err = "User does not exist")
                    response = make_response(html)
                    return response
                if ret == -2:
                    html = render_template('index.html', err = "Incorrect Password")
                    response = make_response(html)
                    return response
                if ret == -3:
                    html = render_template('index.html', err = "Please enter your e-mail and password")
                    response = make_response(html)
                    return response
        else:
            username = None


        if 'search' in request.form:
            search_phrase = request.form['search']
            results = dbf.search(search_phrase)
            if results == None:
                results = {}
        else:
            results = dbf.search('')
            if results == None:
                results = {}

        if 'title' in request.form:
            create_session = {}
            create_session['title'] = request.form['title']
            create_session['description'] = request.form['description']
            create_session['bio'] = request.form['bio']
            create_session['time'] = request.form['time']
            create_session['date'] = request.form['date']
            create_session['max_parps'] = request.form['max_parps']
            dbf.create_workshop(create_session)
            return redirect(url_for('main'))

        if 'button_id' in request.form:
            dbf.sign_up(request.form['button_id'])
            redirect(url_for('main'))

        print(results)

        html = render_template('main.html', results=results, is_host = dbf.is_host, is_signed_up = dbf.is_signed_up)

        response = make_response(html)

        return response

    if request.method == 'GET':
        search_phrase = request.args.get('search')
        button_id = request.args.get('button_id')
        if search_phrase == None:
            results = dbf.search('')
        else:
            results = dbf.search(search_phrase)
        if button_id != None:
            dbf.sign_up(button_id)

        html = render_template('main.html', results=results, is_host = dbf.is_host, is_signed_up = dbf.is_signed_up)

        response = make_response(html)

        return response


#-----------------------------------------------------------------------

@app.route('/my_workshops', methods = ['GET', 'POST'])
def my_workshops():

    if session['username'] is None:
        redirect(url_for('index'))

    username = request.args.get("username")
    signed_up_workshops = dbf.get_signed_workshops()
    created_workshops = dbf.get_my_workshops()
    remove_id = request.args.get('remove_id')
    cancel_id = request.args.get('cancel_id')
    if remove_id != None:
        dbf.remove_workshop(remove_id)
        return redirect(url_for('my_workshops'))
    if cancel_id != None:
        dbf.cancel(cancel_id)
        return redirect(url_for('my_workshops'))

    if 'title' in request.form:
        create_session = {}
        create_session['title'] = request.form['title']
        create_session['description'] = request.form['description']
        create_session['bio'] = request.form['bio']
        create_session['time'] = request.form['time']
        create_session['date'] = request.form['date']
        create_session['max_parps'] = request.form['max_parps']
        dbf.create_workshop(create_session)
        return redirect(url_for('my_workshops'))

    html = render_template('my_workshops.html', username= username, signed_up_workshops = signed_up_workshops, created_workshops = created_workshops)
    response = make_response(html)

    return response

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'register_username' in request.form:
            if 'register_password' in request.form:
                # pw_hash = bcrypt.generate_password_hash(request.form['register_password'])
                ret = dbf.register(
                request.form['register_username'],
                request.form['register_password']
                )
                if ret == -1:
                    html = render_template('index.html', err = "Your email has already been used")
                    response = make_response(html)
                    return response
                if ret == -2:
                    html = render_template('index.html', err = "Please enter a username and password")
                    response = make_response(html)
                    return response
                else:
                    html = render_template('index.html', err = "Registration successful!")
                    response = make_response(html)
                    return response
