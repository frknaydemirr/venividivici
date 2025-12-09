from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, BLOB, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


# Many to many relationship tables

class Question_Categories(Base):
    __tablename__ = 'question_categories'
    question_id = Column(Integer, ForeignKey('questions.question_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'), primary_key=True)


class City_Subscriptions(Base):
    __tablename__ = 'city_subscriptions'
    city_id = Column(Integer, ForeignKey('cities.city_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

class Country_Subscriptions(Base):
    __tablename__ = 'country_subscriptions'
    country_id = Column(Integer, ForeignKey('countries.country_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)


# Voting tables

class Question_Votes(Base):
    __tablename__ = 'question_votes'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    user_of_question_vote = relationship('Users', back_populates='question_votes_of_user')

    question_id = Column(Integer, ForeignKey('questions.question_id'), primary_key=True)
    question_of_vote = relationship('Questions', back_populates='votes_of_question')
    
    vote_type = Column(Boolean, nullable=False)

class Answer_Votes(Base):
    __tablename__ = 'answer_votes'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    user_of_answer_vote = relationship('Users', back_populates='answer_votes_of_user')

    answer_id = Column(Integer, ForeignKey('answers.answer_id'), primary_key=True)
    answer_of_vote = relationship('Answers', back_populates='votes_of_answer')
    vote_type = Column(Boolean, nullable=False)

class Reply_Votes(Base):
    __tablename__ = 'reply_votes'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    user_of_reply_vote = relationship('Users', back_populates='reply_votes_of_user')

    reply_id = Column(Integer, ForeignKey('replies.reply_id'), primary_key=True)
    reply_of_vote = relationship('Replies', back_populates='votes_of_reply')
    vote_type = Column(Boolean, nullable=False)


# Base tables

class Countries(Base):
    __tablename__ = 'countries'
    country_id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(String(256), nullable=False)
    country_img_url = Column(String(256))
    country_info = Column(String(10000))

    cities_of_country = relationship('Cities', back_populates='country_of_city')

    subscribed_users = relationship('Users', secondary='country_subscriptions', back_populates='subscribed_countries')


class Cities(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(256), nullable=False)
    city_img_url = Column(String(256))
    city_info = Column(String(10000))

    country_id = Column(Integer, ForeignKey('countries.country_id'), nullable=False)
    country_of_city = relationship('Countries', back_populates='cities_of_country')

    questions_of_city = relationship('Questions', back_populates='city_of_question')

    users_of_city = relationship('Users', back_populates='city_of_user')

    subscribed_users = relationship('Users', secondary='city_subscriptions', back_populates='subscribed_cities')


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
    city_of_user = relationship('Cities', back_populates='users_of_city')

    questions_of_user = relationship('Questions', back_populates='user_of_question')
    answers_of_user = relationship('Answers', back_populates='user_of_answer')
    replies_of_user = relationship('Replies', back_populates='user_of_reply')

    question_votes_of_user = relationship('Question_Votes', back_populates='user_of_question_vote')
    answer_votes_of_user = relationship('Answer_Votes', back_populates='user_of_answer_vote')
    reply_votes_of_user = relationship('Reply_Votes', back_populates='user_of_reply_vote')

    subscribed_cities = relationship('Cities', secondary='city_subscriptions', back_populates='subscribed_users')
    subscribed_countries = relationship('Countries', secondary='country_subscriptions', back_populates='subscribed_users')


class Categories(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_label = Column(String(64), nullable=False, unique=True)

    questions_of_category = relationship('Questions', secondary='question_categories', backref='categories_of_question')


class Questions(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    time_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    question_title = Column(String(150), nullable=False)
    question_body = Column(String(5000), nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    user_of_question = relationship('Users', back_populates='questions_of_user')

    city_id = Column(Integer, ForeignKey('cities.city_id'), nullable=False)
    city_of_question = relationship('Cities', back_populates='questions_of_city')

    answers_of_question = relationship('Answers', back_populates='question_of_answer')

    votes_of_question = relationship('Question_Votes', back_populates='question_of_vote')

    categories_of_question = relationship('Categories', secondary='question_categories', backref='questions_of_category')


class Answers(Base):
    __tablename__ = 'answers'
    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    answer_body = Column(String(5000), nullable=False)
    time_created = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    user_of_answer = relationship('Users', back_populates='answers_of_user')

    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)
    question_of_answer = relationship('Questions', back_populates='answers_of_question')

    replies_of_answer = relationship('Replies', back_populates='answer_of_reply')

    votes_of_answer = relationship('Answer_Votes', back_populates='answer_of_vote')


class Replies(Base):
    __tablename__ = 'replies'
    reply_id = Column(Integer, primary_key=True, autoincrement=True)
    reply_body = Column(String(2500), nullable=False)
    time_created = Column(DateTime, default=datetime.utcnow, nullable=False)

    answer_id = Column(Integer, ForeignKey('answers.answer_id'), nullable=False)
    answer_of_reply = relationship('Answers', back_populates='replies_of_answer')

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    user_of_reply = relationship('Users', back_populates='replies_of_user')

    votes_of_reply = relationship('Reply_Votes', back_populates='reply_of_vote')