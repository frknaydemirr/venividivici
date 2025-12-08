from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, BLOB, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


# Many to many relationship tables

question_categories = Table('question_categories', Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.question_id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.category_id'), primary_key=True)
)

question_votes = Table('question_votes', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('questions.question_id'), primary_key=True),
    Column('vote_type', Boolean, nullable=False)
)

answer_votes = Table('answer_votes', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answers.answer_id'), primary_key=True),
    Column('vote_type', Boolean, nullable=False)
)

reply_votes = Table('reply_votes', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('reply_id', Integer, ForeignKey('replies.reply_id'), primary_key=True),
    Column('vote_type', Boolean, nullable=False)
)

city_subscriptions = Table('city_subscriptions', Base.metadata,
    Column('city_id', Integer, ForeignKey('cities.city_id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True)
)

country_subscriptions = Table('country_subscriptions', Base.metadata,
    Column('country_id', Integer, ForeignKey('countries.country_id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True)
)


# Base tables

class Countries(Base):
    __tablename__ = 'countries'
    country_id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(String(256), nullable=False)
    country_img_url = Column(String(256))
    country_info = Column(String(10000))


class Cities(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(256), nullable=False)
    city_img_url = Column(String(256))
    city_info = Column(String(10000))

    country_id = Column(Integer, ForeignKey('countries.country_id'), nullable=False)


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False, unique=True)
    full_name = Column(String(64))
    e_mail_addr = Column(String(254), nullable=False, unique=True)
    time_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_img = Column(BLOB)
    password_hash = Column(String(128), nullable=False)
    
    city_id = Column(Integer, ForeignKey('cities.city_id'))


class Categories(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_label = Column(String(64), nullable=False, unique=True)


class Questions(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    time_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    question_title = Column(String(150), nullable=False)
    question_body = Column(String(5000), nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.city_id'), nullable=False)


class Answers(Base):
    __tablename__ = 'answers'
    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    answer_body = Column(String(5000), nullable=False)
    time_created = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)
    

class Replies(Base):
    __tablename__ = 'replies'
    reply_id = Column(Integer, primary_key=True, autoincrement=True)
    reply_body = Column(String(2500), nullable=False)
    time_created = Column(DateTime, default=datetime.utcnow, nullable=False)

    answer_id = Column(Integer, ForeignKey('answers.answer_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    