from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Engine(object):

    __instance = None

    def __init__(self, memory_only: bool=False):
        name = 'sqlite:///lectures' if not memory_only else 'sqlite:///:memory:'
        self.engine = create_engine(name, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @staticmethod
    def get_instance(memory_only: bool=False):
        if Engine.__instance is None:
            Engine.__instance = Engine(memory_only)
        return Engine.__instance


class Lecture(Base):

    __tablename__ = 'lecture'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    content = Column(Text)
    course = Column(String, index=True)


class Summarization(Base):

    __tablename__ = 'summarization'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lecture = Column(Integer, ForeignKey('lecture.id'))
    name = Column(String, index=True)
    ratio = Column(Float)
    content = Column(Text)




