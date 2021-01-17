# -------------------------------------------------------------------------------
# dbf.py
# Description: Back-end API for dynamic front-end development.
# -------------------------------------------------------------------------------

from studygroup.models import User, Workshop
from studygroup import db
from sys import stderr, exit
from studygroup.routes import username
from sqlalchemy import or_

def get_user():
    if username is None:
        err = 'Username was not entered'
        print(err, file=stderr)
        exit(1)
    return User.query.filter_by(email=username).first()

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
        ws.participants.add()

    except:
        err = 'Workshop creation failed'
        print(err, file=stderr)
        return err

    db.session.add(ws)
    db.session.commit()

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
    return username == User.query.get(ws.host).email

# --------------------------------------------------


def get_my_workshops():
    user = get_user()
    if user is None:
        err = 'User not found'
        print(err, file=stderr)
        return err

    wss = user.my_workshops()
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
    user = get_user()
    if user is None:
        err = 'User not found'
        print(err, file=stderr)
        return err

    wss = user.workshops
    res = []
    for id in wss:
        ws = Workshop.query.get(id)
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


def search(phrase):
    user = get_user()
    if user is None:
        err = 'User not found'
        print(err, file=stderr)
        return err

    wss = db.session.query(Workshop).filter(
        or_(
            Workshop.title.ilike(phrase),
            Workshop.description.ilike(phrase)
        )
    ).order_by(
        Workshop.time.desc()
    ).order_by(
        Workshop.date.desc()
    )
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
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()


def is_logged_in():
    return username is not None


def is_registered(username):
    return User.query.filter_by(User.email == username)

