from peewee import Model, CharField, PrimaryKeyField, IntegerField, AutoField
from db.config import db

class Orgs(Model):
    organisation_id = PrimaryKeyField(AutoField())
    organisation_name = CharField()
    organisation_type = CharField()
    organisation_description = CharField()
    organisation_email = CharField()
    password = CharField()
    
    class Meta:
        database = db
        table_name = "Organisation"
        
        
def create():
    db.connect()
    db.create_tables([Orgs])