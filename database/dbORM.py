from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Country(Base):
    __tablename__ = 'Countries'
    Country_id = Column(Integer, primary_key=True)
    Countryname = Column(String(100), nullable=False)
    Countryimg = Column(String(255))
    Countryinfo = Column(String)

    Cities = relationship("City", back_populates="Country")
    UserSubscriptions = relationship("CountrySubscription", back_populates="Country")

class City(Base):
    __tablename__ = 'Cities'
    City_id = Column(Integer, primary_key=True)
    Country_id = Column(Integer, ForeignKey('Countries.Country_id'), nullable=False)
    Cityname = Column(String(100), nullable=False)
    Cityimg = Column(String(255))
    Cityinfo = Column(String)

    Country = relationship("Country", back_populates="Cities")
    Users = relationship("User", back_populates="City")
    UserSubscriptions = relationship("CitySubscription", back_populates="City")



class User(Base):
    __tablename__ = 'Users'
    User_id = Column(Integer, primary_key=True)
    UserName = Column(String(50), nullable=False, unique=True)
    FullName = Column(String(100))
    EmailAddress = Column(String(100), nullable=False, unique=True)
    Password_Hash = Column(String(255), nullable=False)
    Time_Created = Column(DateTime)
    User_img = Column(String(255))
    City_id = Column(Integer, ForeignKey('Cities.City_id'))

    City = relationship("City", back_populates="Users")
    
    Questions_Asked = relationship("Question", back_populates="Asker") 
    Answers_Given = relationship("Answer", back_populates="Responder")
    Replies_Made = relationship("Reply", back_populates="Replier")
    
    Question_Votes = relationship("QuestionVote", back_populates="User")
    Answer_Votes = relationship("AnswerVote", back_populates="User")
    Reply_Votes = relationship("ReplyVote", back_populates="User")
    
    Country_Subscriptions = relationship("CountrySubscription", back_populates="User")
    City_Subscriptions = relationship("CitySubscription", back_populates="User")


class Category(Base):
    __tablename__ = 'Categories'
    Category_id = Column(Integer, primary_key=True)
    Categoryname = Column(String(100), nullable=False, unique=True)
    Categoryimg = Column(String(255))
    
    Question_Categories = relationship("QuestionCategory", back_populates="Category")

class Question(Base):
    __tablename__ = 'Questions'
    Question_id = Column(Integer, primary_key=True)
    User_id = Column(Integer, ForeignKey('Users.User_id'), nullable=False) 
    Question_Title = Column(String(255), nullable=False)
    Question_Body = Column(String)
    Time_Created = Column(DateTime)

    Asker = relationship("User", back_populates="Questions_Asked")
    Answers = relationship("Answer", back_populates="Question") 
    Categories = relationship("QuestionCategory", back_populates="Question")
    Votes = relationship("QuestionVote", back_populates="Question")

class Answer(Base):
    __tablename__ = 'Answers'
    Answer_id = Column(Integer, primary_key=True)
    Question_id = Column(Integer, ForeignKey('Questions.Question_id'), nullable=False)
    User_id = Column(Integer, ForeignKey('Users.User_id'), nullable=False) 
    AnswerBody = Column(String)
    TimeCreated = Column(DateTime)
    
    Question = relationship("Question", back_populates="Answers")
    Responder = relationship("User", back_populates="Answers_Given")
    Replies = relationship("Reply", back_populates="Answer")
    Votes = relationship("AnswerVote", back_populates="Answer")

class Reply(Base):
    __tablename__ = 'Replies'
    Reply_id = Column(Integer, primary_key=True)
    Answer_id = Column(Integer, ForeignKey('Answers.Answer_id'), nullable=False) 
    User_id = Column(Integer, ForeignKey('Users.User_id'), nullable=False) 
    ReplyBody = Column(String)
    TimeCreated = Column(DateTime)
    
    Answer = relationship("Answer", back_populates="Replies")
    Replier = relationship("User", back_populates="Replies_Made")
    Votes = relationship("ReplyVote", back_populates="Reply")


class QuestionCategory(Base):
    __tablename__ = 'QuestionCategories'
    Question_id = Column(Integer, ForeignKey('Questions.Question_id'), primary_key=True)
    Category_id = Column(Integer, ForeignKey('Categories.Category_id'), primary_key=True)
    
    Question = relationship("Question", back_populates="Categories")
    Category = relationship("Category", back_populates="Question_Categories")

class CountrySubscription(Base):
    __tablename__ = 'CountrySubscriptions'
    User_id = Column(Integer, ForeignKey('Users.User_id'), primary_key=True)
    Country_id = Column(Integer, ForeignKey('Countries.Country_id'), primary_key=True)
    
    User = relationship("User", back_populates="Country_Subscriptions")
    Country = relationship("Country", back_populates="UserSubscriptions")

class CitySubscription(Base):
    __tablename__ = 'CitySubscriptions'
    User_id = Column(Integer, ForeignKey('Users.User_id'), primary_key=True)
    City_id = Column(Integer, ForeignKey('Cities.City_id'), primary_key=True)
    
    User = relationship("User", back_populates="City_Subscriptions")
    City = relationship("City", back_populates="UserSubscriptions")

class QuestionVote(Base):
    __tablename__ = 'QuestionVotes'
    User_id = Column(Integer, ForeignKey('Users.User_id'), primary_key=True)
    Question_id = Column(Integer, ForeignKey('Questions.Question_id'), primary_key=True)
    Vote_Type = Column(Boolean)

    User = relationship("User", back_populates="Question_Votes")
    Question = relationship("Question", back_populates="Votes")

class AnswerVote(Base):
    __tablename__ = 'AnswerVotes'
    User_id = Column(Integer, ForeignKey('Users.User_id'), primary_key=True)
    Answer_id = Column(Integer, ForeignKey('Answers.Answer_id'), primary_key=True)
    Vote_Type = Column(Boolean)

    User = relationship("User", back_populates="Answer_Votes")
    Answer = relationship("Answer", back_populates="Votes")

class ReplyVote(Base):
    __tablename__ = 'ReplyVotes'
    User_id = Column(Integer, ForeignKey('Users.User_id'), primary_key=True)
    Reply_id = Column(Integer, ForeignKey('Replies.Reply_id'), primary_key=True)
    Vote_Type = Column(Boolean)

    User = relationship("User", back_populates="Reply_Votes")
    Reply = relationship("Reply", back_populates="Votes")