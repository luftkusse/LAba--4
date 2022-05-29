from sqlalchemy import PrimaryKeyConstraint

from app import db
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, index=True)

    id_admin = db.Column(db.Integer)

    username = db.Column(db.String(50))

    balance = db.Column(db.Float)




class UserAndShare(db.Model):
    __tablename__ = 'usershare'
    __table_args__ = (PrimaryKeyConstraint('user_id', 'share_id'),)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    share_id = db.Column(db.Integer, db.ForeignKey("share.id"))

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True, index=True)
    text_review = db.Column(db.String(50))
    share_id = db.Column(db.Integer, db.ForeignKey('share.id'))

class Share(db.Model):
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True, index=True)
    share_name = db.Column(db.String(50), index=True)
    country = db.Column(db.String(50))
    price = db.Column(db.Float)

class Requests(db.Model):
    __tablename__ = 'requests'
    count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, primary_key=True, index=True)






