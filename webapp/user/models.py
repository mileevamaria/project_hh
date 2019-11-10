from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.db import db


assoc_skill_user = db.Table("assoc_skill_user",
                            db.Column("user_id", db.Integer,
                                      db.ForeignKey("users.id")),
                            db.Column("skill_id", db.Integer, db.ForeignKey("skills.id")))

assoc_area_user = db.Table("assoc_area_user",
                            db.Column("user_id", db.Integer,
                                      db.ForeignKey("users.id")),
                            db.Column("area_id", db.Integer, db.ForeignKey("prof_areas.id")))

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    first_name = db.Column(db.String(80), nullable=True, server_default='Имя')
    last_name = db.Column(db.String(80), nullable=True,
                          server_default='Фамилия')
    city = db.Column(db.String(80), nullable=True, server_default='Город')
    user = db.relationship('Skill', secondary=assoc_skill_user,
                           backref=db.backref('user', lazy='dynamic'))
    user_1 = db.relationship('ProfessionalArea', secondary=assoc_area_user,
                           backref=db.backref('user', lazy='dynamic'))
    favourites = db.relationship('Favourite', backref='user_favourite')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User {}>'.format(self.username)
