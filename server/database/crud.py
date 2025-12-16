# TODO : Check and fix ALL POST helpers

from sqlalchemy.orm import Session, Query
from .models import *
from sqlalchemy import func

from datetime import datetime

class Converter:
    city_query_fields: tuple = (
        Cities.city_id,
        Cities.city_name,
        Cities.city_img_url,
        Cities.city_info  
    )

    country_query_fields: tuple = (
        Countries.country_id,
        Countries.country_name,
        Countries.country_img_url,
        Countries.country_info
    )

    question_query_fields: tuple = (
        Questions.question_id,
        Questions.question_title,
        Questions.question_body,
        Users.username,
        Questions.time_created,
        Questions.city_id,
        Cities.country_id
    )

    answer_query_fields: tuple = (
        Answers.answer_id,
        Answers.answer_body,
        Users.username,
        Answers.time_created,
        Answers.question_id
    )

    reply_query_fields: tuple = (
        Replies.reply_id,
        Replies.reply_body,
        Users.username,
        Replies.time_created,
        Replies.answer_id
    )

    categories_query_fields: tuple = (
        Categories.category_id,
        Categories.category_label
    )

    categories_with_stats_fields: tuple = (
        Categories.category_id,
        Categories.category_label,
        func.count(Questions.question_id).label('question_count'),
        func.count(Answers.answer_id).label('answer_count')
    )

    @staticmethod
    def city_query_to_list(cities_query: Query) -> list:
        city_list = []
        
        for city in cities_query:
            city_list.append({
                "city-id": city.city_id,
                "city-name": city.city_name,
                "url": city.city_img_url,
                "info": city.city_info
            })
        
        return city_list

    @staticmethod
    def country_query_to_list(countries_query: Query) -> list:
        country_list = []
        
        for country in countries_query:
            country_list.append({
                "country-id": country.country_id,
                "country-name": country.country_name,
                "url": country.country_img_url,
                "info": country.country_info
            })
        
        return country_list

    @staticmethod
    def question_query_to_list(questions_query: Query) -> list:
        question_list = []

        for question in questions_query:
            question_list.append({
                "question-id": question.question_id,
                "question-title": question.question_title,
                "question-body": question.question_body,
                "username": question.username,
                "creation-time": question.time_created,
                "city-id": question.city_id,
                "country-id": question.country_id
            })

        return question_list

    @staticmethod
    def answer_query_to_list(answers_query: Query) -> list:
        answer_list = []

        for answer in answers_query:
            answer_list.append({
                "answer-id": answer.answer_id,
                "answer-body": answer.answer_body,
                "answered-by": answer.username,
                "creation-time": answer.time_created,
                "question-id": answer.question_id
            })

        return answer_list

    @staticmethod
    def reply_query_to_list(replies_query: Query) -> list:
        reply_list = []

        for reply in replies_query:
            reply_list.append({
                "reply-id": reply.reply_id,
                "reply-body": reply.reply_body,
                "replied-by": reply.username,
                "creation-time": reply.time_created,
                "answer-id": reply.answer_id
            })

        return reply_list

    @staticmethod
    def categories_query_to_list(categories_query: Query) -> list:
        categories_list = []
        
        for category in categories_query:
            categories_list.append({
                "category-id": category.category_id,
                "category-label": category.category_label
            })
        
        return categories_list

    @staticmethod
    def categories_with_stats_query_to_list(categories_query: Query) -> list:
        categories_list = []

        for category in categories_query:
            categories_list.append({
                "category-id": category.category_id,
                "category-label": category.category_label,
                "question-count": category.question_count,
                "answer-count": category.answer_count
            })
        
        return categories_list


class Database:
    def __init__(self, session: Session):
        self.__session = session

    ############### GET ###############

    def get_specific_city(self, city_id: int) -> dict:
        city = self.__session.query(*Converter.city_query_fields)\
            .filter(Cities.city_id == city_id).first()
        
        if not city:
            return {}

        return {
            "city-id": city.city_id,
            "city-name": city.city_name,
            "url": city.city_img_url,
            "info": city.city_info
        }

    def get_city_question_and_answer_counts(self, city_id: int) -> dict:
        question_count = self.__session.query(
            func.count(Questions.question_id)
        )\
            .filter(Questions.active == True) \
            .filter(Questions.city_id == city_id).scalar()

        answer_count = self.__session.query(
            func.count(Answers.answer_id)
        )\
            .filter(Answers.active == True) \
            .join(Questions, Answers.question_id == Questions.question_id) \
            .filter(Questions.city_id == city_id).scalar()

        if question_count is None or answer_count is None:
            return {}

        return {
            "question-count": question_count,
            "answer-count": answer_count
        }

    def get_cities_in_specific_country(self, country_id: int, offset: int, limit: int) -> list:
        cities = self.__session.query(*Converter.city_query_fields) \
            .filter(Cities.country_id == country_id) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not cities:
            return []
        
        return Converter.city_query_to_list(cities)

    def get_most_conquered_cities(self, limit: int) -> list:
        cities = self.__session.query(*Converter.city_query_fields) \
            .outerjoin(Questions, Cities.city_id == Questions.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .filter(Questions.active == True) \
            .group_by(Cities.city_id) \
            .order_by((func.count(Questions.question_id) + func.count(Answers.answer_id)).desc()) \
            .limit(limit) \
            .all()

        if not cities:
            return []

        return Converter.city_query_to_list(cities)

    def get_cities_matching_query(self, query_string: str, offset: int, limit: int) -> list:
        cities = self.__session.query(*Converter.city_query_fields) \
            .filter(Cities.city_name.ilike(f"%{query_string}%")) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not cities:
            return []

        return Converter.city_query_to_list(cities)

    def get_subscribed_cities(self, user_id: int) -> list:
        user = self.__session.query(Users) \
            .filter(Users.user_id == user_id) \
            .filter(Users.active == True) \
            .first()

        if not user:
            return []

        return Converter.city_query_to_list(user.subscribed_cities)

    


    def get_all_countries(self) -> list:
        countries = self.__session.query(
            Countries.country_id,
            Countries.country_name       
        ).all()

        if not countries:
            return []
        
        country_list = []

        for country in countries:
            country_list.append({
                "country-id": country.country_id,
                "country-name": country.country_name
            })

        return country_list

    def get_country_question_and_answer_counts(self, country_id: int) -> dict:
        question_count = self.__session.query(
            func.count(Questions.question_id)
        )\
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Questions.active == True) \
            .filter(Cities.country_id == country_id) \
            .scalar()

        answer_count = self.__session.query(
            func.count(Answers.answer_id)
        )\
            .join(Questions, Answers.question_id == Questions.question_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Answers.active == True) \
            .filter(Cities.country_id == country_id) \
            .scalar()

        if question_count is None or answer_count is None:
            return {}

        return {
            "question-count": question_count,
            "answer-count": answer_count
        }

    def get_specific_country(self, country_id: int) -> dict:
        country = self.__session.query(*Converter.country_query_fields)\
            .filter(Countries.country_id == country_id).first()
        
        if not country:
            return {}

        return {
            "country-id": country.country_id,
            "country-name": country.country_name,
            "url": country.country_img_url,
            "info": country.country_info
        }

    def get_most_conquered_countries(self, limit: int) -> list:
        countries = self.__session.query(*Converter.country_query_fields) \
            .outerjoin(Cities, Countries.country_id == Cities.country_id) \
            .outerjoin(Questions, Cities.city_id == Questions.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .filter(Questions.active == True) \
            .group_by(Countries.country_id) \
            .order_by((func.count(Questions.question_id) + func.count(Answers.answer_id)).desc()) \
            .limit(limit) \
            .all()

        if not countries:
            return []

        return Converter.country_query_to_list(countries)

    def get_countries_matching_query(self, query_string: str, offset: int, limit: int):
        countries = self.__session.query(*Converter.country_query_fields) \
            .filter(Countries.country_name.ilike(f"%{query_string}%")) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not countries:
            return []
        
        return Converter.country_query_to_list(countries)


    def get_subscribed_countries(self, user_id: int) -> list:
        user = self.__session.query(Users) \
            .filter(Users.user_id == user_id) \
            .filter(Users.active == True) \
            .first()

        if not user:
            return []

        return Converter.country_query_to_list(user.subscribed_countries)

    def get_specific_question(self, question_id: int) -> dict:
        question = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Questions.question_id == question_id) \
            .filter(Questions.active == True) \
            .first()

        if not question:
            return {}

        return {
            "question-id": question.question_id,
            "question-title": question.question_title,
            "question-body": question.question_body,
            "username": question.username,
            "creation-time": question.time_created,
            "city-id": question.city_id,
            "country-id": question.country_id
        }


    def get_question_answer_and_vote_counts(self, question_id: int) -> dict:
        answer_count = self.__session.query(
            func.count(Answers.answer_id)
        )\
            .filter(Answers.question_id == question_id) \
            .filter(Answers.active == True) \
            .scalar()

        upvote_count = self.__session.query(
            func.count(Question_Votes.vote_type)
        )\
            .filter(Question_Votes.question_id == question_id) \
            .filter(Question_Votes.vote_type == True) \
            .filter(Question_Votes.active == True) \
            .scalar()

        downvote_count = self.__session.query(
            func.count(Question_Votes.vote_type)
        )\
            .filter(Question_Votes.question_id == question_id) \
            .filter(Question_Votes.vote_type == False) \
            .filter(Question_Votes.active == True) \
            .scalar()

        if answer_count is None or upvote_count is None or downvote_count is None:
            return {}

        return {
            "answer-count": answer_count,
            "vote-count": upvote_count - downvote_count
        }

    def get_most_answered_questions(self, offset: int, limit: int) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .filter(Questions.active == True) \
            .group_by(Questions.question_id) \
            .order_by(func.count(Answers.answer_id).desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not questions:
            return []

        return Converter.question_query_to_list(questions)

    def get_categories_of_question(self, question_id: int) -> list:
        categories = self.__session.query(*Converter.categories_query_fields) \
            .join(Question_Categories, Categories.category_id == Question_Categories.category_id) \
            .filter(Question_Categories.question_id == question_id) \
            .filter(Question_Categories.active == True) \
            .all()

        if not categories:
            return []

        return Converter.categories_query_to_list(categories)

    def get_most_answered_questions_in_city(self, city_id: int, offset: int, limit: int) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .filter(Questions.city_id == city_id) \
            .filter(Questions.active == True) \
            .group_by(Questions.question_id) \
            .order_by(func.count(Answers.answer_id).desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not questions:
            return []

        return Converter.question_query_to_list(questions)

    def get_most_answered_questions_in_country(self, country_id: int, offset: int, limit: int) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .filter(Cities.country_id == country_id) \
            .filter(Questions.active == True) \
            .group_by(Questions.question_id) \
            .order_by(func.count(Answers.answer_id).desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not questions:
            return []

        return Converter.question_query_to_list(questions)

    def get_recent_questions(self, offset: int, limit: int) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .order_by(Questions.time_created.desc()) \
            .filter(Questions.active == True) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not questions:
            return []

        return Converter.question_query_to_list(questions)

    def get_recent_questions_of_city(self, city_id: int, offset: int, limit: int) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Questions.city_id == city_id) \
            .filter(Questions.active == True) \
            .order_by(Questions.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not questions:
            return []

        return Converter.question_query_to_list(questions)

    def get_recent_questions_of_country(self, country_id: int, offset: int, limit: int) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Cities.country_id == country_id) \
            .filter(Questions.active == True) \
            .order_by(Questions.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not questions:
            return []

        return Converter.question_query_to_list(questions)

    def get_questions_matching_query(self, query_string: str, offset: int, limit: int) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Questions.question_title.ilike(f"%{query_string}%") | Questions.question_body.ilike(f"%{query_string}%")) \
            .filter(Questions.active == True) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not questions:
            return []

        return Converter.question_query_to_list(questions)

    def get_questions_from_subscriptions(self, user_id: int, offset: int, limit: int) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .join(City_Subscriptions, Questions.city_id == City_Subscriptions.city_id) \
            .join(Country_Subscriptions, Cities.country_id == Country_Subscriptions.country_id) \
            .filter(
                (City_Subscriptions.user_id == user_id) |
                (Country_Subscriptions.user_id == user_id)
            ) \
            .filter(Questions.active == True) \
            .order_by(Questions.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not questions:
            return []

        return Converter.question_query_to_list(questions)

    def get_questions_of_user(self, username: str, offset: 0, limit: 10) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .filter(Users.username == username) \
            .filter(Questions.active == True) \
            .order_by(Questions.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not questions:
            return []

        return Converter.question_query_to_list(questions)

    

    def get_specific_answer(self, answer_id: int) -> dict:
        answer = self.__session.query(*Converter.answer_query_fields) \
            .join(Users, Answers.user_id == Users.user_id) \
            .filter(Answers.answer_id == answer_id) \
            .filter(Answers.active == True) \
            .first()

        if not answer:
            return {}

        return {
            "answer-id": answer.answer_id,
            "answer-body": answer.answer_body,
            "username": answer.username,
            "creation-time": answer.time_created,
            "question-id": answer.question_id
        }

    

    def get_answer_vote_and_reply_counts(self, answer_id: int) -> dict:
        reply_count = self.__session.query(
            func.count(Replies.reply_id)
        )\
            .filter(Replies.answer_id == answer_id) \
            .filter(Replies.active == True) \
            .scalar()

        upvote_count = self.__session.query(
            func.count(Answer_Votes.answer_id)
        )\
            .filter(Answer_Votes.answer_id == answer_id) \
            .filter(Answer_Votes.active == True) \
            .filter(Answer_Votes.vote_type == True) \
            .scalar()

        downvote_count = self.__session.query(
            func.count(Answer_Votes.answer_id)
        )\
            .filter(Answer_Votes.answer_id == answer_id) \
            .filter(Answer_Votes.vote_type == False) \
            .filter(Answer_Votes.active == True) \
            .scalar()

        if reply_count is None or upvote_count is None or downvote_count is None:
            return {}

        return {
            "reply-count": reply_count,
            "vote-count": upvote_count - downvote_count
        }

    def get_answers_of_specific_question(self, question_id: int, offset: int, limit: int) -> list:
        answers = self.__session.query(*Converter.answer_query_fields) \
            .join(Users, Answers.user_id == Users.user_id) \
            .filter(Answers.question_id == question_id) \
            .filter(Answers.active == True) \
            .order_by(Answers.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not answers:
            return []

        return Converter.answer_query_to_list(answers)

    def get_answers_of_user(self, username: str, offset: 0, limit: 10) -> list:
        answers = self.__session.query(*Converter.answer_query_fields) \
            .join(Users, Answers.user_id == Users.user_id) \
            .filter(Users.username == username) \
            .filter(Users.active == True) \
            .order_by(Answers.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()
        
        if not answers:
            return []

        return Converter.answer_query_to_list(answers)

    def get_specific_reply(self, reply_id: int):
        reply = self.__session.query(
            Replies.reply_id,
            Replies.reply_body,
            Users.username,
            Replies.time_created,
            Replies.answer_id
        ) \
            .join(Users, Replies.user_id == Users.user_id) \
            .filter(Replies.reply_id == reply_id) \
            .filter(Replies.active == True) \
            .first()

        if not reply:
            return {}

        return {
            "reply-id": reply.reply_id,
            "reply-body": reply.reply_body,
            "username": reply.username,
            "creation-time": reply.time_created,
            "answer-id": reply.answer_id
        }

    

    

    def get_replies_of_specific_answer(self, answer_id: int, offset: int, limit: int) -> list:
        replies = self.__session.query(*Converter.reply_query_fields) \
            .join(Users, Replies.user_id == Users.user_id) \
            .filter(Replies.answer_id == answer_id) \
            .filter(Replies.active == True) \
            .order_by(Replies.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not replies:
            return []

        return Converter.reply_query_to_list(replies)

    def get_replies_of_user(self, username: str, offset: 0, limit: 10) -> list:
        replies = self.__session.query(*Converter.reply_query_fields) \
            .join(Users, Replies.user_id == Users.user_id) \
            .filter(Users.username == username) \
            .filter(Users.active == True) \
            .order_by(Replies.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        if not replies:
            return []

        return Converter.reply_query_to_list(replies)

    def get_vote_counts_for_specific_reply(self, reply_id: int) -> dict:
        upvote_count = self.__session.query(
            func.count(Reply_Votes.reply_id)
        ) \
            .filter(Reply_Votes.reply_id == reply_id) \
            .filter(Reply_Votes.active == True) \
            .filter(Reply_Votes.vote_type == True) \
            .scalar()

        downvote_count = self.__session.query(
            func.count(Reply_Votes.reply_id)
        ) \
            .filter(Reply_Votes.reply_id == reply_id) \
            .filter(Reply_Votes.active == True) \
            .filter(Reply_Votes.vote_type == False) \
            .scalar()

        if upvote_count is None or downvote_count is None:
            return {}

        return {
            "vote-count": upvote_count - downvote_count
        }

    def get_all_categories(self) -> list:
        Categories = self.__session.query(*Converter.categories_query_fields) \
            .all()

        if not Categories:
            return []

        return Converter.categories_query_to_list(Categories)
        
    def get_specific_category(self, category_id: int) -> dict:
        category = self.__session.query(*Converter.categories_query_fields) \
            .filter(Categories.category_id == category_id) \
            .first()

        if not category:
            return {}

        return {
            "category-id": category.category_id,
            "category-label": category.category_label
        }

    def get_all_categories_of_city_with_stats(self, city_id: int) -> list:
        categories = self.__session.query(*Converter.categories_with_stats_fields) \
            .join(Question_Categories, Categories.category_id == Question_Categories.category_id) \
            .join(Questions, Question_Categories.question_id == Questions.question_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .filter(Questions.city_id == city_id) \
            .filter(Questions.active == True) \
            .group_by(Categories.category_id) \
            .all()

        if not categories:
            return []

        return Converter.categories_with_stats_query_to_list(categories)    

    def get_all_categories_of_country_with_stats(self, country_id: int) -> list:
        categories = self.__session.query(*Converter.categories_with_stats_fields) \
            .join(Question_Categories, Categories.category_id == Question_Categories.category_id) \
            .join(Questions, Question_Categories.question_id == Questions.question_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .filter(Cities.country_id == country_id) \
            .filter(Questions.active == True) \
            .group_by(Categories.category_id) \
            .all()

        if not categories:
            return []

        return Converter.categories_with_stats_query_to_list(categories)

    def get_user_info(self, username: int) -> dict:
        user = self.__session.query(
            Users.city_id,
            Users.username,
            Users.time_created
        ) \
            .filter(Users.username == username) \
            .filter(Users.active == True) \
            .first()

        if not user:
            return {}

        return {
            "username": user.username,
            "creation-time": user.time_created,
            "city-id": user.city_id
        }

    def get_user_exists(self, username: str) -> bool:
        user = self.__session.query(Users.user_id) \
            .filter(Users.username == username) \
            .filter(Users.active == True) \
            .first()
        
        return user is not None

    def get_user_password_match(self, username: str, password: str) -> bool:
        user = self.__session.query(Users.password) \
            .filter(Users.username == username) \
            .filter(Users.active == True) \
            .first()
        
        if user:
            return user.password == password
        else:
            return False

    def get_user_id(self, username: str) -> int:
        user = self.__session.query(Users.user_id) \
            .filter(Users.username == username) \
            .filter(Users.active == True) \
            .first()
        
        if user:
            return user.user_id
        else:
            return None

    def get_user_vote_for_question(self, user_id: int, question_id: int) -> dict:
        vote = self.__session.query(Question_Votes.vote_type) \
            .filter(Question_Votes.user_id == user_id) \
            .filter(Question_Votes.question_id == question_id) \
            .filter(Users.active == True) \
            .first()
        
        if vote:
            return {"vote-type": vote.vote_type}
        else:
            return {}

    def get_user_vote_for_answer(self, user_id: int, answer_id: int) -> dict:
        vote = self.__session.query(Answer_Votes.vote_type) \
            .filter(Answer_Votes.user_id == user_id) \
            .filter(Answer_Votes.answer_id == answer_id) \
            .filter(Answer_Votes.active == True) \
            .first()
        
        if vote:
            return {"vote-type": vote.vote_type}
        else:
            return {}

    def get_user_vote_for_reply(self, user_id: int, reply_id: int) -> dict:
        vote = self.__session.query(Reply_Votes.vote_type) \
            .filter(Reply_Votes.user_id == user_id) \
            .filter(Reply_Votes.reply_id == reply_id) \
            .filter(Reply_Votes.active == True) \
            .first()
        
        if vote:
            return {"vote-type": vote.vote_type}
        else:
            return {}

    

    ################# DELETE / DEACTIVATE #################

    def delete_specific_question(self, question_id: int) -> bool:
        question: Questions = self.__session.query(Questions) \
            .filter(Questions.question_id == question_id) \
            .filter(Questions.active == True) \
            .first()
        
        if question:
            question.active = False
        else:
            return False

        # Deactivate all votes of the question
        votes_of_question = self.__session.query(Question_Votes) \
            .filter(Question_Votes.question_id == question_id) \
            .filter(Question_Votes.active == True) \
            .all()

        for vote in votes_of_question:
            vote.active = False

        # Deactivate all answers of the question
        answers_of_question = self.__session.query(Answers.answer_id) \
            .filter(Answers.question_id == question_id) \
            .filter(Answers.active == True) \
            .all()

        for answer in answers_of_question:
            self.delete_specific_answer(answer.answer_id)

        # Deactivate all categories of the question
        categories_of_question = self.__session.query(Question_Categories) \
            .filter(Question_Categories.question_id == question_id) \
            .filter(Question_Categories.active == True) \
            .all()

        for category in categories_of_question:
            category.active = False

        self.__session.commit()
        return True


    def delete_specific_answer(self, answer_id: int) -> bool:
        answer: Answers = self.__session.query(Answers) \
            .filter(Answers.answer_id == answer_id) \
            .filter(Answers.active == True) \
            .first()
        
        if answer:
            answer.active = False
        else:
            return False

        # Deactivate all votes of the answer
        votes_of_answer = self.__session.query(Answer_Votes) \
            .filter(Answer_Votes.answer_id == answer_id) \
            .filter(Answer_Votes.active == True) \
            .all()

        for vote in votes_of_answer:
            vote.active = False

        # Deactivate all replies of the answer
        replies_of_answer = self.__session.query(Replies.reply_id) \
            .filter(Replies.answer_id == answer_id) \
            .filter(Replies.active == True) \
            .all()

        for reply in replies_of_answer:
            self.delete_specific_reply(reply.reply_id)
        
        self.__session.commit()
        return True


    def delete_specific_reply(self, reply_id: int) -> bool:
        reply: Replies = self.__session.query(Replies) \
            .filter(Replies.reply_id == reply_id) \
            .filter(Replies.active == True) \
            .first()
        
        if reply:
            reply.active = False
        else:
            return False

        # Deactivate all votes of the reply
        votes_of_reply = self.__session.query(Reply_Votes) \
            .filter(Reply_Votes.reply_id == reply_id) \
            .filter(Reply_Votes.active == True) \
            .all()

        for vote in votes_of_reply:
            vote.active = False

        self.__session.commit()
        return True


    def delete_user_vote_for_question(self, user_id: int, question_id: int):
        existing_vote = self.__session.query(Question_Votes) \
            .filter(Question_Votes.user_id == user_id) \
            .filter(Question_Votes.question_id == question_id) \
            .filter(Question_Votes.active == True) \
            .first()
        
        if existing_vote:
            self.__session.delete(existing_vote)
            self.__session.commit()


    def delete_user_vote_for_answer(self, user_id: int, answer_id: int):
        existing_vote = self.__session.query(Answer_Votes) \
            .filter(Answer_Votes.user_id == user_id) \
            .filter(Answer_Votes.answer_id == answer_id) \
            .filter(Answer_Votes.active == True) \
            .first()
        
        if existing_vote:
            self.__session.delete(existing_vote)
            self.__session.commit()


    def delete_user_vote_for_reply(self, user_id: int, reply_id: int):
        existing_vote = self.__session.query(Reply_Votes) \
            .filter(Reply_Votes.user_id == user_id) \
            .filter(Reply_Votes.reply_id == reply_id) \
            .filter(Reply_Votes.active == False) \
            .first()
        
        if existing_vote:
            self.__session.delete(existing_vote)
            self.__session.commit()



    ################# POST #################

    def post_subscribe_city(self, user_id: int, city_id: int, subscription_type: bool):
        city = self.__session.query(Cities) \
            .filter(Cities.city_id == city_id) \
            .first()
        
        if subscription_type:
            user.subscribed_cities.append(city)
        else:
            user.subscribed_cities.remove(city)
        
        self.__session.commit()

    def post_subscribe_country(self, user_id: int, country_id: int, subscription_type: bool):
        country = self.__session.query(Countries) \
            .filter(Countries.country_id == country_id) \
            .first()
        
        if subscription_type:
            user.subscribed_countries.append(country)
        else:
            user.subscribed_countries.remove(country)
        
        self.__session.commit()

    def post_new_question(self, user_id: int, city_id: int, question_title: str, question_body: str, category_ids: list) -> int:
        new_question = Questions(
            user_id=user_id,
            city_id=city_id,
            question_title=question_title,
            question_body=question_body,
            time_created=datetime.utcnow()
        )
        self.__session.add(new_question)
        self.__session.commit()

        for category_id in category_ids:
            category = self.__session.query(Categories) \
                .filter(Categories.category_id == category_id) \
                .first()
            new_question.categories_of_question.append(category)
        
        self.__session.commit()

        new_question_id = self.__session.query(Questions.question_id) \
            .filter(Questions.user_id == user_id) \
            .filter(Questions.city_id == city_id) \
            .filter(Questions.question_title == question_title) \
            .filter(Questions.question_body == question_body) \
            .first()

        return new_question_id.question_id

    def post_new_answer(self, user_id: int, question_id: int, answer_body: str) -> int:
        new_answer = Answers(
            user_id=user_id,
            question_id=question_id,
            answer_body=answer_body,
            time_created=datetime.utcnow()
        )
        self.__session.add(new_answer)
        self.__session.commit()

        new_answer = self.__session.query(Answers.answer_id) \
            .filter(Answers.user_id == user_id) \
            .filter(Answers.question_id == question_id) \
            .filter(Answers.answer_body == answer_body) \
            .first()

        return new_answer.answer_id
    
    
    def post_new_reply(self, user_id: int, answer_id: int, reply_body: str) -> int:
        new_reply = Replies(
            user_id=user_id,
            answer_id=answer_id,
            reply_body=reply_body,
            time_created=datetime.utcnow()
        )
        self.__session.add(new_reply)
        self.__session.commit()

        new_reply = self.__session.query(Replies.reply_id) \
            .filter(Replies.user_id == user_id) \
            .filter(Replies.answer_id == answer_id) \
            .filter(Replies.reply_body == reply_body) \
            .first()

        return new_reply.reply_id


    def post_user_vote_for_question(self, user_id: int, question_id: int, vote_type: bool):
        existing_vote = self.__session.query(Question_Votes) \
            .filter(Question_Votes.user_id == user_id) \
            .filter(Question_Votes.question_id == question_id) \
            .first()
        
        if existing_vote:
            existing_vote.vote_type = vote_type
        else:
            new_vote = Question_Votes(
                user_id=user_id,
                question_id=question_id,
                vote_type=vote_type
            )
            self.__session.add(new_vote)
        
        self.__session.commit()

    def post_user_vote_for_answer(self, user_id: int, answer_id: int, vote_type: bool):
        existing_vote = self.__session.query(Answer_Votes) \
            .filter(Answer_Votes.user_id == user_id) \
            .filter(Answer_Votes.answer_id == answer_id) \
            .first()
        
        if existing_vote:
            existing_vote.vote_type = vote_type
        else:
            new_vote = Answer_Votes(
                user_id=user_id,
                answer_id=answer_id,
                vote_type=vote_type
            )
            self.__session.add(new_vote)
        
        self.__session.commit()

    def post_user_vote_for_reply(self, user_id: int, reply_id: int, vote_type: bool):
        existing_vote = self.__session.query(Reply_Votes) \
            .filter(Reply_Votes.user_id == user_id) \
            .filter(Reply_Votes.reply_id == reply_id) \
            .first()
        
        if existing_vote:
            existing_vote.vote_type = vote_type
        else:
            new_vote = Reply_Votes(
                user_id=user_id,
                reply_id=reply_id,
                vote_type=vote_type
            )
            self.__session.add(new_vote)
        
        self.__session.commit()