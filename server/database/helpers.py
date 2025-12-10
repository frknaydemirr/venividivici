from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, Query
from server.database.definitions import *
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
    def __init__(self, database_server_url: str):
        self.__engine = create_engine(database_server_url)
        self.__Session = sessionmaker(bind=self.__engine)
        self.__session = self.__Session()

    def get_specific_city(self, city_id: int) -> dict:
        city = self.__session.query(*Converter.question_query_fields)\
            .filter(Cities.city_id == city_id).first()
        
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
            .filter(Questions.city_id == city_id).scalar()

        answer_count = self.__session.query(
            func.count(Answers.answer_id)
        )\
            .join(Questions, Answers.question_id == Questions.question_id) \
            .filter(Questions.city_id == city_id).scalar()

        return {
            "question-count": question_count,
            "answer-count": answer_count
        }

    def get_cities_in_specific_country(self, country_id: int, offset: int = 0, limit: int = 10) -> list:
        cities = self.__session.query(*Converter.city_query_fields) \
            .filter(Cities.country_id == country_id) \
            .offset(offset) \
            .limit(limit) \
            .all()
        
        return Converter.city_query_to_list(cities)

    def get_most_conquered_cities(self, limit: int = 10) -> list:
        cities = self.__session.query(*Converter.city_query_fields) \
            .outerjoin(Questions, Cities.city_id == Questions.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .group_by(Cities.city_id) \
            .order_by((func.count(Questions.question_id) + func.count(Answers.answer_id)).desc()) \
            .limit(limit) \
            .all()

        return Converter.city_query_to_list(cities)

    def get_cities_matching_query(self, query_string: str, offset: int = 0, limit: int = 10):
        cities = self.__session.query(*Converter.city_query_fields) \
            .filter(Cities.city_name.ilike(f"%{query_string}%")) \
            .offset(offset) \
            .limit(limit) \
            .all()
        
        return Converter.city_query_to_list(cities)

    def get_subscribed_cities(self, user_id: int) -> list:
        user = self.__session.query(Users) \
            .filter(Users.user_id == user_id) \
            .first()

        return Converter.city_query_to_list(user.subscribed_cities)

    def post_subscribe_city(self, user_id: int, city_id: int, subscription_type: bool):
        user = self.__session.query(Users) \
            .filter(Users.user_id == user_id) \
            .first()
        
        city = self.__session.query(Cities) \
            .filter(Cities.city_id == city_id) \
            .first()
        
        if subscription_type:
            user.subscribed_cities.append(city)
        else:
            user.subscribed_cities.remove(city)
        
        self.__session.commit()

    def get_all_countries(self) -> list:
        countries = self.__session.query(
            Countries.country_id,
            Countries.country_name       
        ).all()
        
        return Converter.country_query_to_list(countries)

    def get_country_question_and_answer_counts(self, country_id: int) -> dict:
        question_count = self.__session.query(
            func.count(Questions.question_id)
        )\
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Cities.country_id == country_id).scalar()

        answer_count = self.__session.query(
            func.count(Answers.answer_id)
        )\
            .join(Questions, Answers.question_id == Questions.question_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Cities.country_id == country_id).scalar()

        return {
            "question-count": question_count,
            "answer-count": answer_count
        }

    def get_specific_country(self, country_id: int) -> dict:
        country = self.__session.query(*Converter.country_query_fields)\
            .filter(Countries.country_id == country_id).first()
        
        return {
            "country-id": country.country_id,
            "country-name": country.country_name,
            "url": country.country_img_url,
            "info": country.country_info
        }

    def get_most_conquered_countries(self, country_id: int) -> list:
        countries = self.__session.query(*Converter.country_query_fields) \
            .outerjoin(Cities, Countries.country_id == Cities.country_id) \
            .outerjoin(Questions, Cities.city_id == Questions.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .group_by(Countries.country_id) \
            .order_by((func.count(Questions.question_id) + func.count(Answers.answer_id)).desc()) \
            .limit(country_id) \
            .all()

        return Converter.country_query_to_list(countries)

    def get_countries_matching_query(self, query_string: str, offset: int = 0, limit: int = 10):
        countries = self.__session.query(*Converter.country_query_fields) \
            .filter(Countries.country_name.ilike(f"%{query_string}%")) \
            .offset(offset) \
            .limit(limit) \
            .all()
        
        return Converter.country_query_to_list(countries)

    def get_subscribed_countries(self, user_id: int) -> list:
        user = self.__session.query(Users) \
            .filter(Users.user_id == user_id) \
            .first()

        return Converter.country_query_to_list(user.subscribed_countries)

    def post_subscribe_country(self, user_id: int, country_id: int, subscription_type: bool):
        user = self.__session.query(Users) \
            .filter(Users.user_id == user_id) \
            .first()
        
        country = self.__session.query(Countries) \
            .filter(Countries.country_id == country_id) \
            .first()
        
        if subscription_type:
            user.subscribed_countries.append(country)
        else:
            user.subscribed_countries.remove(country)
        
        self.__session.commit()

    def post_new_question(self, user_id: int, city_id: int, question_title: str, question_body: str, category_ids: list):
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

    def get_specific_question(self, question_id: int) -> dict:
        question = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Questions.question_id == question_id) \
            .first()

        return {
            "question-id": question.question_id,
            "question-title": question.question_title,
            "question-body": question.question_body,
            "asked-by": question.username,
            "creation-time": question.time_created,
            "city-id": question.city_id,
            "country-id": question.country_id
        }

    def delete_specific_question(self, question_id: int):
        question = self.__session.query(Questions) \
            .filter(Questions.question_id == question_id) \
            .first()
        
        self.__session.delete(question)
        self.__session.commit()

    def get_question_answer_and_vote_counts(self, question_id: int) -> dict:
        answer_count = self.__session.query(
            func.count(Answers.answer_id)
        )\
            .filter(Answers.question_id == question_id).scalar()

        upvote_count = self.__session.query(
            func.count(Question_Votes.vote_id)
        )\
            .filter(Question_Votes.question_id == question_id) \
            .filter(Question_Votes.vote_type == True).scalar()

        downvote_count = self.__session.query(
            func.count(Question_Votes.vote_id)
        )\
            .filter(Question_Votes.question_id == question_id) \
            .filter(Question_Votes.vote_type == False).scalar()

        return {
            "answer-count": answer_count,
            "vote-count": upvote_count - downvote_count
        }

    def get_most_answered_questions(self, offset: int = 0, limit: int = 10) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .group_by(Questions.question_id) \
            .order_by(func.count(Answers.answer_id).desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.question_query_to_list(questions)

    def get_categories_of_question(self, question_id: int) -> list:
        categories = self.__session.query(*Converter.categories_query_fields) \
            .join(question_categories, Categories.category_id == question_categories.c.category_id) \
            .filter(question_categories.c.question_id == question_id) \
            .all()

        return Converter.categories_query_to_list(categories)

    def get_most_answered_questions_in_city(self, city_id: int, offset: int = 0, limit: int = 10) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .filter(Questions.city_id == city_id) \
            .group_by(Questions.question_id) \
            .order_by(func.count(Answers.answer_id).desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.question_query_to_list(questions)

    def get_most_answered_questions_in_country(self, country_id: int, offset: int = 0, limit: int = 10) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .filter(Cities.country_id == country_id) \
            .group_by(Questions.question_id) \
            .order_by(func.count(Answers.answer_id).desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.question_query_to_list(questions)

    def get_recent_questions(self, offset: int = 0, limit: int = 10) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .order_by(Questions.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.question_query_to_list(questions)

    def get_recent_questions_of_city(self, city_id: int, offset: int = 0, limit: int = 10) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Questions.city_id == city_id) \
            .order_by(Questions.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.question_query_to_list(questions)

    def get_recent_questions_of_country(self, country_id: int, offset: int = 0, limit: int = 10) -> list:
        Questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Cities.country_id == country_id) \
            .order_by(Questions.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.question_query_to_list(Questions)

    def get_questions_matching_query(self, query_string: str, offset: int = 0, limit: int = 10) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Questions.question_title.ilike(f"%{query_string}%") | Questions.question_body.ilike(f"%{query_string}%")) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.question_query_to_list(questions)

    def get_questions_from_subscriptions(self, user_id: int, offset: int = 0, limit: int = 10) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .join(city_subscriptions, Questions.city_id == city_subscriptions.c.city_id) \
            .join(country_subscriptions, Cities.country_id == country_subscriptions.c.country_id) \
            .filter(
                (city_subscriptions.c.user_id == user_id) |
                (country_subscriptions.c.user_id == user_id)
            ) \
            .order_by(Questions.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.question_query_to_list(questions)

    def get_questions_of_user(self, user_id: int, offset: 0, limit: 10) -> list:
        questions = self.__session.query(*Converter.question_query_fields) \
            .join(Users, Questions.user_id == Users.user_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .filter(Questions.user_id == user_id) \
            .order_by(Questions.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.question_query_to_list(questions)

    def post_new_answer(self, user_id: int, question_id: int, answer_body: str):
        new_answer = Answers(
            user_id=user_id,
            question_id=question_id,
            answer_body=answer_body,
            time_created=datetime.utcnow()
        )
        self.__session.add(new_answer)
        self.__session.commit()

    def get_specific_answer(self, answer_id: int) -> dict:
        answer = self.__session.query(*Converter.answer_query_fields) \
            .join(Users, Answers.user_id == Users.user_id) \
            .filter(Answers.answer_id == answer_id) \
            .first()

        return {
            "answer-id": answer.answer_id,
            "answer-body": answer.answer_body,
            "answered-by": answer.username,
            "creation-time": answer.time_created,
            "question-id": answer.question_id
        }

    def delete_specific_answer(self, answer_id: int):
        answer = self.__session.query(Answers) \
            .filter(Answers.answer_id == answer_id) \
            .first()
        
        self.__session.delete(answer)
        self.__session.commit()

    def get_answer_vote_and_reply_counts(self, answer_id: int) -> dict:
        reply_count = self.__session.query(
            func.count(Replies.reply_id)
        )\
            .filter(Replies.answer_id == answer_id).scalar()

        upvote_count = self.__session.query(
            func.count(Answer_Votes.vote_id)
        )\
            .filter(Answer_Votes.answer_id == answer_id) \
            .filter(Answer_Votes.vote_type == True).scalar()

        downvote_count = self.__session.query(
            func.count(Answer_Votes.vote_id)
        )\
            .filter(Answer_Votes.answer_id == answer_id) \
            .filter(Answer_Votes.vote_type == False).scalar()

        return {
            "reply-count": reply_count,
            "vote-count": upvote_count - downvote_count
        }

    def get_answers_of_specific_question(self, question_id: int, offset: int = 0, limit: int = 10) -> list:
        answers = self.__session.query(*Converter.answer_query_fields) \
            .join(Users, Answers.user_id == Users.user_id) \
            .filter(Answers.question_id == question_id) \
            .order_by(Answers.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.answer_query_to_list(answers)

    def get_answers_of_user(self, user_id: int, offset: 0, limit: 10) -> list:
        answers = self.__session.query(*Converter.answer_query_fields) \
            .join(Users, Answers.user_id == Users.user_id) \
            .filter(Answers.user_id == user_id) \
            .order_by(Answers.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

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
            .first()

        return {
            "reply-id": reply.reply_id,
            "reply-body": reply.reply_body,
            "replied-by": reply.username,
            "creation-time": reply.time_created,
            "answer-id": reply.answer_id
        }

    def post_new_reply(self, user_id: int, answer_id: int, reply_body: str):
        new_reply = Replies(
            user_id=user_id,
            answer_id=answer_id,
            reply_body=reply_body,
            time_created=datetime.utcnow()
        )
        self.__session.add(new_reply)
        self.__session.commit()

    def delete_specific_reply(self, reply_id: int):
        reply = self.__session.query(Replies) \
            .filter(Replies.reply_id == reply_id) \
            .first()
        
        self.__session.delete(reply)
        self.__session.commit()

    def get_replies_of_specific_answer(self, answer_id: int, offset: int = 0, limit: int = 10) -> list:
        replies = self.__session.query(*Converter.reply_query_fields) \
            .join(Users, Replies.user_id == Users.user_id) \
            .filter(Replies.answer_id == answer_id) \
            .order_by(Replies.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.reply_query_to_list(replies)

    def get_replies_of_user(self, user_id: int, offset: 0, limit: 10) -> list:
        replies = self.__session.query(*Converter.reply_query_fields) \
            .join(Users, Replies.user_id == Users.user_id) \
            .filter(Replies.user_id == user_id) \
            .order_by(Replies.time_created.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return Converter.reply_query_to_list(replies)

    def get_vote_counts_for_specific_reply(self, reply_id: int) -> dict:
        upvote_count = self.__session.query(
            func.count(Reply_Votes.vote_id)
        ) \
            .filter(Reply_Votes.reply_id == reply_id) \
            .filter(Reply_Votes.vote_type == True).scalar()

        downvote_count = self.__session.query(
            func.count(Reply_Votes.vote_id)
        ) \
            .filter(Reply_Votes.reply_id == reply_id) \
            .filter(Reply_Votes.vote_type == False).scalar()

        return {
            "vote-count": upvote_count - downvote_count
        }

    def get_all_categories(self) -> list:
        Categories = self.__session.query(*Converter.categories_query_fields) \
            .all()

        return Converter.categories_query_to_list(Categories)
        
    def get_specific_category(self, category_id: int) -> dict:
        category = self.__session.query(*Converter.categories_query_fields) \
            .filter(Categories.category_id == category_id) \
            .first()

        return {
            "category-id": category.category_id,
            "category-label": category.category_label
        }

    def get_all_categories_of_city_with_stats(self, city_id: int) -> list:
        categories = self.__session.query(*Converter.categories_with_stats_fields) \
            .join(question_categories, Categories.category_id == question_categories.c.category_id) \
            .join(Questions, question_categories.c.question_id == Questions.question_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .filter(Questions.city_id == city_id) \
            .group_by(Categories.category_id) \
            .all()

        return Converter.categories_with_stats_query_to_list(categories)    

    def get_all_categories_of_country_with_stats(self, country_id: int) -> list:
        categories = self.__session.query(*Converter.categories_with_stats_fields) \
            .join(question_categories, Categories.category_id == question_categories.c.category_id) \
            .join(Questions, question_categories.c.question_id == Questions.question_id) \
            .join(Cities, Questions.city_id == Cities.city_id) \
            .outerjoin(Answers, Questions.question_id == Answers.question_id) \
            .filter(Cities.country_id == country_id) \
            .group_by(Categories.category_id) \
            .all()

        return Converter.categories_with_stats_query_to_list(categories)

    def get_user_info(self, user_id: int) -> dict:
        user = self.__session.query(
            Users.user_id,
            Users.username,
            Users.time_created
        ) \
            .filter(Users.user_id == user_id) \
            .first()

        return {
            "user-id": user.user_id,
            "username": user.username,
            "creation-time": user.time_created
        }

    def get_user_vote_for_question(self, user_id: int, question_id: int) -> bool:
        vote = self.__session.query(Question_Votes.vote_type) \
            .filter(Question_Votes.user_id == user_id) \
            .filter(Question_Votes.question_id == question_id) \
            .first()
        
        if vote:
            return vote.vote_type
        else:
            return None

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

    def delete_user_vote_for_question(self, user_id: int, question_id: int):
        existing_vote = self.__session.query(Question_Votes) \
            .filter(Question_Votes.user_id == user_id) \
            .filter(Question_Votes.question_id == question_id) \
            .first()
        
        if existing_vote:
            self.__session.delete(existing_vote)
            self.__session.commit()

    def get_user_vote_for_answer(self, user_id: int, answer_id: int) -> bool:
        vote = self.__session.query(Answer_Votes.vote_type) \
            .filter(Answer_Votes.user_id == user_id) \
            .filter(Answer_Votes.answer_id == answer_id) \
            .first()
        
        if vote:
            return vote.vote_type
        else:
            return None

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

    def delete_user_vote_for_answer(self, user_id: int, answer_id: int):
        existing_vote = self.__session.query(Answer_Votes) \
            .filter(Answer_Votes.user_id == user_id) \
            .filter(Answer_Votes.answer_id == answer_id) \
            .first()
        
        if existing_vote:
            self.__session.delete(existing_vote)
            self.__session.commit()

    def get_user_vote_for_reply(self, user_id: int, reply_id: int) -> bool:
        vote = self.__session.query(Reply_Votes.vote_type) \
            .filter(Reply_Votes.user_id == user_id) \
            .filter(Reply_Votes.reply_id == reply_id) \
            .first()
        
        if vote:
            return vote.vote_type
        else:
            return None

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

    def delete_user_vote_for_reply(self, user_id: int, reply_id: int):
        existing_vote = self.__session.query(Reply_Votes) \
            .filter(Reply_Votes.user_id == user_id) \
            .filter(Reply_Votes.reply_id == reply_id) \
            .first()
        
        if existing_vote:
            self.__session.delete(existing_vote)
            self.__session.commit()