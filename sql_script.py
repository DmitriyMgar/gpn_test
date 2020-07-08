from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from model import Event, Journal

engine = create_engine('sqlite:///journals.db', echo=True)
session_db = sessionmaker(bind=engine)
session = session_db()

query = session.query(Journal, Event)
query = query.join(Event, Event.code == Journal.event_code)
query = query.distinct(Journal.user_id)
records = query.all()
for journal, event in records:
    print(journal)
print(1)
