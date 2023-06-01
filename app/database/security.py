from flask_security import UserMixin, RoleMixin
from flask_security import SQLAlchemyUserDatastore

from app.database.base import sa

class RolesUsers(sa.Model):
    __bind_key__ = "qms"
    __tablename__ = 'employees_to_roles'
    id = sa.Column('ID', sa.Integer, primary_key=True)
    user_id = sa.Column('employee', sa.Integer, sa.ForeignKey('employees.ID'))
    role_id = sa.Column('role', sa.Integer, sa.ForeignKey('roles.ID'))
    evaluation_date = sa.Column('Evaluation Date', sa.Date)

class Role(sa.Model, RoleMixin):
    __bind_key__ = "qms"
    __tablename__ = 'roles'
    id = sa.Column('ID', sa.Integer, primary_key=True)
    name = sa.Column('Title', sa.String)
    description = sa.Column('Description', sa.String)

class User(sa.Model, UserMixin):
    __bind_key__ = 'qms'
    __tablename__ = 'employees'
    id = sa.Column('ID', sa.Integer, primary_key=True)
    email = sa.Column(sa.String)
    username = sa.Column('name', sa.String)
    password = sa.Column(sa.String)
    active = sa.Column(sa.Boolean)
    fs_uniquifier = sa.Column(sa.String)
    status = sa.Column(sa.Integer, sa.ForeignKey('employment status.ID'))

user_datastore = SQLAlchemyUserDatastore(sa, User, Role)
