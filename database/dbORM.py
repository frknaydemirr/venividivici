from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, BLOB, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Many to many relationship tables

question_categories = Table('question-categories', Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.question_id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.category_id'), primary_key=True)
)

question_votes = Table('question-votes', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('questions.question_id'), primary_key=True),
    Column('vote_type', Boolean, nullable=False)
)

answer_votes = Table('answer-votes', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answers.answer_id'), primary_key=True),
    Column('vote_type', Boolean, nullable=False)
)

reply_votes = Table('reply-votes', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('reply_id', Integer, ForeignKey('replies.reply_id'), primary_key=True),
    Column('vote_type', Boolean, nullable=False)
)

city_subscriptions = Table('city-subscriptions', Base.metadata,
    Column('city_id', Integer, ForeignKey('cities.city_id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True)
)

country_subscriptions = Table('country-subscriptions', Base.metadata,
    Column('country_id', Integer, ForeignKey('countries.country_id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True)
)

class Countries(Base):
    __tablename__ = 'countries'
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String(256), nullable=False)
    country_img = Column(BLOB)
    country_info = Column(String(10000))

    cities = relationship('Cities', back_populates='country')


class Cities(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(256), nullable=False)
    city_img = Column(BLOB)
    city_info = Column(String(10000))

    country_id = Column(Integer, ForeignKey('countries.country_id'), nullable=False)
    country = relationship('Countries', back_populates='cities', uselist=False)
    
    users_of_city = relationship('Users', back_populates='city_of_user')
    questions_of_city = relationship('Questions', back_populates='city_of_question')

    user_subscriptions_of_city = relationship('Users', secondary=city_subscriptions, back_populates='city_subscription_of_users')
    user_subscriptions_of_country = relationship('Users', secondary=country_subscriptions, back_populates='country_subscription_of_users')


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    full_name = Column(String(64))
    e_mail_addr = Column(String(254), nullable=False, unique=True)
    time_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_img = Column(BLOB)
    password_hash = Column(String(128), nullable=False)
    
    city_id = Column(Integer, ForeignKey('cities.city_id'))
    city_of_user = relationship('Cities', back_populates='users_of_city', uselist=False)
    
    questions_of_user = relationship('Questions', back_populates='user_of_question')
    answers_of_user = relationship('Answers', back_populates='user_of_answer')
    replies_of_user = relationship('Replies', back_populates='user_of_reply')
    
    question_votes_of_users = relationship('Questions', secondary=question_votes, back_populates='users_votes_of_question')
    answer_votes_of_users = relationship('Answers', secondary=answer_votes, back_populates='users_votes_of_answer')
    reply_votes_of_users = relationship('Replies', secondary=reply_votes, back_populates='users_votes_of_reply')

    city_subscription_of_users = relationship('Cities', secondary=city_subscriptions, back_populates='user_subscriptions_of_city')
    country_subscription_of_users = relationship('Countries', secondary=country_subscriptions, back_populates='user_subscriptions_of_country')


class Categories(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    category_label = Column(String(64), nullable=False, unique=True)

    questions_of_category = relationship('Questions', secondary=question_categories, back_populates='categories_of_question') 


class Questions(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True)
    time_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    question_title = Column(String(150), nullable=False)
    question_body = Column(String(5000), nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    user_of_question = relationship('Users', back_populates='questions_of_user', uselist=False)

    city_id = Column(Integer, ForeignKey('cities.city_id'), nullable=False)
    city_of_question = relationship('Cities', back_populates='questions_of_city', uselist=False)
    
    answers_of_question = relationship('Answers', back_populates='question_of_answer')
    categories_of_question = relationship('Categories', secondary=question_categories, back_populates='questions_of_category')
    users_votes_of_question = relationship('Users', secondary=question_votes, back_populates='question_votes_of_users')


class Answers(Base):
    __tablename__ = 'answers'
    answer_id = Column(Integer, primary_key=True)
    answer_body = Column(String(5000), nullable=False)
    time_created = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    user_of_answer = relationship('Users', back_populates='answers_of_user', uselist=False)

    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)
    question_of_answer = relationship('Questions', back_populates='answers_of_question', uselist=False)
    
    replies_of_answer = relationship('Replies', back_populates='answer_of_reply')
    users_votes_of_answer = relationship('Users', secondary=answer_votes, back_populates='answer_votes_of_users')
    

class Replies(Base):
    __tablename__ = 'replies'
    reply_id = Column(Integer, primary_key=True)
    reply_body = Column(String(2500), nullable=False)
    time_created = Column(DateTime, default=datetime.utcnow, nullable=False)

    answer_id = Column(Integer, ForeignKey('answers.answer_id'), nullable=False)
    answer_of_reply = relationship('Answers', back_populates='replies_of_answer', uselist=False)
    
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    user_of_reply = relationship('Users', back_populates='replies_of_user', uselist=False)
    
    users_votes_of_reply = relationship('Users', secondary=reply_votes, back_populates='reply_votes_of_users')