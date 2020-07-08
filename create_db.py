from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime, json, re

from model import Event, Journal

engine = create_engine('sqlite:///journals.db', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
session_db = sessionmaker(bind=engine)

session = session_db()

with open('codeToText.tsv', encoding='utf8') as events_file:
    for line in events_file:
        line = line.strip().split('\t')
        event = Event(code=line[0], name=line[1])
        if session.query(Event).filter_by(code=event.code).count() == 0:
            session.add(event)
            session.commit()

with open('journals_shot.tsv', encoding='utf8') as journal:
    journal_columns = journal.readline().split()
    for line in journal:
        line = line.strip().split('\t')
        journal = dict(zip(journal_columns, line))
        if(re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{1,6}').match(journal['eventTime'])):
            journal['eventTime'] = datetime.datetime.strptime(journal['eventTime'], '%Y-%m-%d %H:%M:%S.%f')
        elif(re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}').match(journal['eventTime'])):
            journal['eventTime'] = datetime.datetime.strptime(journal['eventTime'], '%Y-%m-%d %H:%M:%S')
        hit = Journal(
            id=journal['id'],
            user_id=journal['userId'],
            event_time=journal['eventTime'],
            event_code=journal['eventCode'],
            content=json.loads(journal['content'].strip('"').replace('""', '"')),
            additional=json.loads(journal['additional'].strip('"').replace('""', '"'))
        )
        if session.query(Journal).filter_by(id=hit.id).count() == 0:
            session.add(hit)
            session.commit()

print(1)

session.close()