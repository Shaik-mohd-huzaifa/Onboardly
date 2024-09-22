from peewee import Model, AutoField, PrimaryKeyField, ForeignKeyField, CharField
from db.config import db
from db.schemas.organsiations import Orgs


class Notes(Model):
    id = PrimaryKeyField(AutoField())
    name = CharField()
    description = CharField()
    Org_id = ForeignKeyField(Orgs, backref="org_rules", on_delete="CASCADE")

    class Meta:
        database = db
        table_name = "Notes"


def create():
    db.connect()
    db.create_tables([Notes])
