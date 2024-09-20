from peewee import Model, AutoField, PrimaryKeyField, ForeignKeyField, CharField, IntegerField
from db.config import db

class Documents(Model):
    document_id = PrimaryKeyField(AutoField())
    document_name = CharField()
    document_description = CharField()
    document_address = CharField()
    
    
    class Meta():
        database = db
        table_name = "Documents"
        
        
def create():
    db.connect()
    db.create_tables([Documents])
    