from peewee import Model, AutoField, PrimaryKeyField, ForeignKeyField, CharField, IntegerField
from db.config import db
from db.schemas.organsiations import Orgs

class Documents(Model):
    document_id = PrimaryKeyField(AutoField())
    document_name = CharField()
    document_description = CharField()
    organisation = ForeignKeyField(Orgs, backref="org_docs", on_delete="CASCADE")
    document_address = CharField()

    class Meta():
        database = db
        table_name = "Documents"


def create():
    db.connect()
    db.create_tables([Documents])
