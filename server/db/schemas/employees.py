from peewee import AutoField, PrimaryKeyField, ForeignKeyField, CharField, Model, BooleanField
from db.schemas.organsiations import Orgs
from db.config import db


class Employees(Model):
    employee_id = PrimaryKeyField(AutoField())
    employee_name = CharField()
    employee_email = CharField()
    password = CharField()
    employee_type = CharField()
    organisation_id = ForeignKeyField(Orgs, backref="onboarding_employees", on_delete="CASCADE")
    onboarding = BooleanField()

    class Meta:
        database = db
        table_name = "employees"
        
def create():
    db.connect()
    db.create_tables([Employees])
    
    