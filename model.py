from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Journal(Base):
    __tablename__ = 'journals'
    id = Column(String, primary_key=True)
    user_id = Column(String)
    event_time = Column(DateTime)
    event_code = Column(String, ForeignKey('events.code'))
    event = relationship('Event', back_populates='journal')
    content = Column(JSON)
    additional = Column(JSON)


class Event(Base):
    __tablename__ = 'events'
    code = Column(String, primary_key=True)
    name = Column(String)
    journal = relationship('Journal', back_populates='event')