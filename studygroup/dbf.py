# -------------------------------------------------------------------------------
# dbf.py
# Description: Back-end API for dynamic front-end development.
# -------------------------------------------------------------------------------

from studygroup.models import User, Workshop
from studygroup import db, bcrypt
from sys import stderr, exit
from sqlalchemy import or_
from flask import session

def get_user():
    if session['username'] is None:
        err = 'Username was not entered'
        print(err, file=stderr)
        exit(1)
    return User.query.filter_by(email=session['username']).first()

# --------------------------------------------------


def create_workshop(info):

    try:
        user = get_user()
        if user is None:
            err = 'User not found'
            print(err, file=stderr)
            return err

        ws = Workshop(
            host=user.id,
            max_participants=info["max_parps"],
            title=info["title"],
            description=info["description"],
            bio=info["bio"],
            date=info["date"],
            time=info["time"]
        )

        db.session.add(ws)
        db.session.commit()

    except:
        err = 'Workshop creation failed'
        print(err, file=stderr)
        return err

# --------------------------------------------------


def remove_workshop(wid):
    ws = Workshop.query.get(wid)
    db.session.delete(ws)
    db.session.commit()

# --------------------------------------------------


def has_free_spots(wid):
    ws = Workshop.query.get(wid)
    return ws.max_participants > ws.num_participants

# --------------------------------------------------


def sign_up(wid):
    if not has_free_spots(wid):
        err = 'Cannot sign up for a full workshop'
        print(err, file=stderr)
        return err

    user = get_user()
    if user is None:
        err = 'User not found'
        print(err, file=stderr)
        return err

    ws = Workshop.query.get(wid)
    ws.num_participants += 1
    ws.participants.append(user)
    db.session.commit()


# --------------------------------------------------


def cancel(wid):
    user = get_user()
    if user is None:
        err = 'User not found'
        print(err, file=stderr)
        return err

    ws = Workshop.query.get(wid)
    ws.num_participants -= 1
    ws.participants.remove(user)
    db.session.commit()


# --------------------------------------------------


def edit_workshop(info, wid):
    user = get_user()
    if user is None:
        err = 'User not found'
        print(err, file=stderr)
        return err

    # ensure that the editor is the host
    ws = Workshop.query.get(wid)
    if not is_host(wid):
        err = 'Not your workshop'
        print(err, file=stderr)
        return err

    ws.max_participants = info["max_parps"]
    ws.title = info["title"]
    ws.description = info["description"]
    ws.bio = info["bio"]
    ws.date = info["date"]
    ws.time = info["time"]
    db.session.commit()

# --------------------------------------------------


def is_host(wid):
    ws = Workshop.query.get(wid)
    return session['username'] == User.query.get(ws.host).email

# --------------------------------------------------


def get_my_workshops():
    user = User.query.filter_by(email=session['username']).first()
    if user is None:
        err = 'User not found'
        print(err, file=stderr)
        return err

    wss = user.my_workshops
    res = []
    for ws in wss:
        res.append(
            {
                "id": ws.id,
                "title": ws.title,
                "date": ws.date,
                "time": ws.time,
                "description": ws.description,
                "num_parps": ws.num_participants,
                "max_parps": ws.max_participants,
                "bio": ws.bio
            }
        )
    return res


def get_signed_workshops():
    user = User.query.filter_by(email=session['username']).first()
    if user is None:
        err = 'User not found'
        print(err, file=stderr)
        return err

    wss = user.workshops
    res = []
    for ws in wss:
        res.append(
            {
                "id": ws.id,
                "title": ws.title,
                "date": ws.date,
                "time": ws.time,
                "description": ws.description,
                "num_parps": ws.num_participants,
                "max_parps": ws.max_participants,
                "bio": ws.bio
            }
        )
    return res

def is_signed_up(wid):
    user = User.query.filter_by(email=session['username']).first()
    ws = Workshop.query.get(wid)
    print(ws.participants)
    return user in ws.participants


def search(phrase):
    user = get_user()
    if user is None:
        err = 'User not found'
        print(err, file=stderr)
        return err

    wss = db.session.query(Workshop).filter(
        or_(
            Workshop.title.ilike("%" + phrase + "%"),
            Workshop.description.ilike("%" + phrase + "%")
        )
    ).order_by(
        Workshop.time.desc()
    ).order_by(
        Workshop.date.desc()
    ).all()
    res = []
    for ws in wss:
        res.append(
            {
                "id": ws.id,
                "title": ws.title,
                "date": ws.date,
                "time": ws.time,
                "description": ws.description,
                "num_parps": ws.num_participants,
                "max_parps": ws.max_participants,
                "bio": ws.bio
            }
        )
    return res


def register(email, password):
    if email is None or password is None or email == "" or password == "":
        return -2

    user = User.query.filter_by(email=email).first()
    if user is not None:
        return -1

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return 0

def login(email, password):
    if email is None or password is None or email == "" or password == "":
        return -3
    user = User.query.filter_by(email=email).first()
    if user is None:
        return -1
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return -2
    session['username'] = email
    return 0


def is_logged_in():
    return session['username'] is not None
