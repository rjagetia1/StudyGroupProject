from studygroup import db
from studygroup.models import User, Workshop

db.drop_all()
db.create_all()
db.session.commit()
