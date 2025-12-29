INSERT INTO users (user_id, username, full_name, e_mail_addr, time_created, password, city_id) VALUES
(1, 'alice', 'Alice A', 'alice@test.com', '2025-11-20 09:10:00', 'md5_like_hash_aaaaaaaaaaaaaaa', NULL), -- Get token testing user
(2, 'vote_user', 'vote user', 'voteuser@test.com', '2025-11-20 09:10:00', 'vote_user_pass', NULL), -- Voting testing user
(3, 'entry_post_delete_user', 'entry post delete user', 'entry_post_delete_user@test.com', '2025-11-21 10:20:00', 'entry_post_delete_user_pass', NULL), -- Entries(question, answer, reply) post-delete testing user
(4, 'sub_user', 'sub user', 'sub_user@test.com', '2025-11-22 11:30:00', 'sub_user_pass', NULL), -- Subscription testing user
(5, 'entry_get_user', 'entry get user', 'entry_get_user@test.com', '2025-11-23 12:40:00', 'entry_get_user_pass', NULL), -- Entries(question, answer, reply) get testing user
(6, 'categories_user', 'categories user', 'categories_user@test.com', '2025-11-24 13:50:00', 'categories_user_pass', NULL), -- Categories testing user
(7, 'questions_user', 'questions user', 'questions_user@test.com', '2025-11-25 14:00:00', 'questions_user_pass', NULL), -- Get questions testing user
(8, 'replies_of_answer_user', 'replies of answer user', 'replies_of_answer_user@test.com', '2025-11-26 15:10:00', 'replies_of_answer_user_pass', NULL), -- Get replies of answer testing user
(9, 'replies_user', 'replies user', 'replies_user@test.com', '2025-11-27 16:20:00', 'replies_user_pass', NULL), -- General replies testing user
(10, 'search_user', 'search user', 'search_user@test.com', '2025-11-28 17:30:00', 'search_user_pass', NULL), -- Search testing user
(11, 'info_user', 'info user', 'info_user@test.com', '2025-11-29 18:40:00', 'info_user_pass', 10); -- User info testing user

INSERT INTO countries (country_id, country_name) VALUES
(1, 'vote_country'), -- Voting testing country
(2, 'entry_post_delete_country'), -- Entries(question, answer, reply) post-delete testing country
(3, 'sub_get_country1'), -- Subscription testing country - 1
(4, 'sub_get_country2'), -- Subscription testing country - 2
(5, 'sub_post_country'), -- Subscription testing country post
(6, 'entry_get_country'), -- Entries(question, answer, reply) get testing country
(7, 'categories_country'), -- Categories testing country
(8, 'get_country'), -- General get testing country
(9, 'questions_user_country'), -- Get questions testing country
(10, 'replies_of_answer_country'), -- Get replies of answer testing country
(11, 'replies_user_country'), -- General replies testing country
(12, 'Search Country'); -- Search testing country

INSERT INTO cities (city_id, city_name, country_id) VALUES
(1, 'vote_city', 1), -- Voting testing city
(2, 'entry_post_delete_city', 2), -- Entries(question, answer, reply) post-delete testing city
(3, 'sub_city1_1', 3), -- Subscription testing city - 1.1
(4, 'sub_city1_2', 3), -- Subscription testing city - 1.2
(5, 'sub_city2_1', 4), -- Subscription testing city - 2.1
(6, 'sub_city2_2', 4), -- Subscription testing city - 2.2
(7, 'sub_post_city', 5), -- Subscription testing city post
(8, 'entry_get_city', 6), -- Entries(question, answer, reply) get testing city
(9, 'categories_city', 7), -- Categories testing city
(10, 'get_city', 8), -- General get testing city
(11, 'questions_user_city', 9), -- Get questions testing city
(12, 'replies_of_answer_city', 10), -- Get replies of answer testing city
(13, 'replies_user_city', 11), -- General replies testing city
(14, 'Search City', 12); -- Search testing city

INSERT INTO questions (question_id, time_created, question_title, question_body, user_id, city_id) VALUES
(1, '2025-12-10 10:15:00', 'vote question title', 'vote question body', 2, 1), -- Voting testing question
(2, '2025-12-11 11:20:00', 'delete question title', 'delete question body', 3, 2), -- Delete testing question
(3, '2025-12-12 12:25:00', 'sub question title 1_1_1', 'sub question body 1_1_1', 4, 3), -- Subscription testing question - 1_1_1
(4, '2025-12-13 13:30:00', 'sub question title 1_1_2', 'sub question body 1_1_2', 4, 3), -- Subscription testing question - 1_1_2
(5, '2025-12-14 14:35:00', 'sub question title 1_2_1', 'sub question body 1_2_1', 4, 4), -- Subscription testing question - 1_2_1
(6, '2025-12-14 14:35:00', 'sub question title 1_2_2', 'sub question body 1_2_2', 4, 4), -- Subscription testing question - 1_2_2
(7, '2025-12-15 15:40:00', 'sub question title 2_1_1', 'sub question body 2_1_1', 4, 5), -- Subscription testing question - 2_1_1
(8, '2025-12-16 16:45:00', 'sub question title 2_1_2', 'sub question body 2_1_2', 4, 5), -- Subscription testing question - 2_1_2
(9, '2025-12-17 17:50:00', 'sub question title 2_2_1', 'sub question body 2_2_1', 4, 6), -- Subscription testing question - 2_2_1
(10,'2025-12-18 18:55:00', 'sub question title 2_2_2', 'sub question body 2_2_2', 4, 6), -- Subscription testing question - 2_2_2
(11,'2025-12-19 19:00:00', 'get question title', 'get question body', 5, 8), -- get testing question
(12,'2025-12-20 20:05:00', 'answers of question title', 'answers question body', 5, 8), -- question for get testing answers
(13,'2025-12-21 21:10:00', 'category question title', 'category question body', 6, 9), -- question for categories testing
(14,'2025-12-22 22:15:00', 'questions user title 1', 'questions user body 1', 7, 11), -- questions user testing question 1
(15,'2025-12-23 23:20:00', 'questions user title 2', 'questions user body 2', 7, 11), -- questions user testing question 2
(16,'2025-12-24 23:25:00', 'replies of answer question title', 'replies of answer question body', 8, 12), -- question for get replies of answer testing
(17,'2025-12-25 23:30:00', 'replies user question title', 'replies user question body', 9, 13), -- general replies testing question
(18,'2025-12-26 23:35:00', 'search question title', 'search question body', 10, 14); -- search testing question

INSERT INTO categories (category_id, category_label) VALUES
(1, 'category_of_question1'), 
(2, 'category_of_question2'), 
(3, 'category_for_nothing'), 
(4, 'specific_category');

INSERT INTO question_categories (question_id, category_id) VALUES
(13, 1),
(13, 2);

INSERT INTO answers (answer_id, answer_body, time_created, user_id, question_id) VALUES
(1,  'vote answer body', '2025-12-10 12:00:00', 2, 1), -- Voting testing answer
(2,  'delete answer body', '2025-12-11 13:00:00', 3, 2), -- Delete testing answer
(3,  'get answer body', '2025-12-19 20:00:00', 5, 11), -- get testing answer
(4,  'first answer of question body', '2025-12-20 21:00:00', 5, 12), -- first answer for get testing answers
(5,  'second answer of question body', '2025-12-20 22:00:00', 5, 12), -- second answer for get testing answers
(6, 'replies of answer answer body', '2025-12-24 23:30:00', 8, 16), -- answer for get replies of answer testing
(7, 'replies user answer body', '2025-12-25 23:40:00', 9, 17); -- answer for general replies testing

INSERT INTO replies (reply_id, reply_body, time_created, answer_id, user_id) VALUES
(1, 'vote reply body', '2025-12-10 12:30:00', 2, 1), -- Voting testing reply
(2, 'delete reply body', '2025-12-11 14:00:00', 2, 3), -- Delete testing reply
(3, 'get reply body', '2025-12-19 21:00:00', 3, 5), -- get testing reply
(4, 'first reply of answer body', '2025-12-24 23:40:00', 6, 8), -- first reply for get replies of answer testing
(5, 'second reply of answer body', '2025-12-24 23:50:00', 6, 8), -- second reply for get replies of answer testing
(6, 'replies user reply body', '2025-12-25 23:50:00', 7, 9); -- reply for general replies testing

INSERT INTO country_subscriptions (country_id, user_id) VALUES
(4, 4);

INSERT INTO city_subscriptions (city_id, user_id) VALUES
(3, 4);

INSERT INTO question_votes (user_id, question_id, vote_type) VALUES
(2, 1, 1);

INSERT INTO answer_votes (user_id, answer_id, vote_type) VALUES
(2, 1, 1);

INSERT INTO reply_votes (user_id, reply_id, vote_type) VALUES
(2, 1, 1);