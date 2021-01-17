# -------------------------------------------------------------------------------
# models.py
# -------------------------------------------------------------------------------

from studygroup import db

# -------------------------------------------------------------------------------

junction_table = db.Table(
    'signups', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('workshop_id', db.Integer, db.ForeignKey('workshop.id')),
)

# -------------------------------------------------------------------------------


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)

    my_workshops = db.relationship('Workshop', backref='host', lazy=True)
    workshops = db.relationship("Workshop", secondary=junction_table)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.password}')"

# -------------------------------------------------------------------------------


class Workshop(db.Model):

    __tablename__ = 'workshop'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    host = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    participants = db.relationship("User", secondary=junction_table)

    max_participants = db.Column(db.Integer, nullable=True)
    num_participants = db.Column(db.Integer, default=0)

    title = db.Column(db.String(254), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    bio = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Workshop('{self.host}', '{self.max_participants}', '{self.num_participants}')"

# -------------------------------------------------------------------------------

