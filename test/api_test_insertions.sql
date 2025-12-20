INSERT INTO users (user_id, username, full_name, e_mail_addr, time_created, password, city_id) VALUES
(1, 'alice', 'Alice A', 'alice@test.com', '2025-11-20 09:10:00', 'md5_like_hash_aaaaaaaaaaaaaaa', NULL), -- Get token testing user
(2, 'vote_user', 'vote user', 'voteuser@test.com', '2025-11-20 09:10:00', 'vote_user_pass', NULL), -- Voting testing user
(3, 'entry_post_delete_user', 'entry post delete user', 'entry_post_delete_user@test.com', '2025-11-21 10:20:00', 'entry_post_delete_user_pass', NULL), -- Entries(question, answer, reply) post-delete testing user
(4, 'sub_user', 'sub user', 'sub_user@test.com', '2025-11-22 11:30:00', 'sub_user_pass', NULL); -- Subscription testing user

INSERT INTO countries (country_id, country_name) VALUES
(1, 'vote_country'), -- Voting testing country
(2, 'entry_post_delete_country'), -- Entries(question, answer, reply) post-delete testing country
(3, 'sub_get_country1'), -- Subscription testing country - 1
(4, 'sub_get_country2'), -- Subscription testing country - 2
(5, 'sub_post_country'); -- Subscription testing country post

INSERT INTO cities (city_id, city_name, country_id) VALUES
(1, 'vote_city', 1), -- Voting testing city
(2, 'entry_post_delete_city', 2), -- Entries(question, answer, reply) post-delete testing city
(3, 'sub_city1_1', 3), -- Subscription testing city - 1.1
(4, 'sub_city1_2', 3), -- Subscription testing city - 1.2
(5, 'sub_city2_1', 4), -- Subscription testing city - 2.1
(6, 'sub_city2_2', 4), -- Subscription testing city - 2.2
(7, 'sub_post_city', 5); -- Subscription testing city post

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
(10,'2025-12-18 18:55:00', 'sub question title 2_2_2', 'sub question body 2_2_2', 4, 6); -- Subscription testing question - 2_2_2

INSERT INTO answers (answer_id, answer_body, time_created, user_id, question_id) VALUES
(1,  'vote answer body', '2025-12-10 12:00:00', 2, 1), -- Voting testing answer
(2,  'delete answer body', '2025-12-11 13:00:00', 3, 2); -- Delete testing answer

INSERT INTO replies (reply_id, reply_body, time_created, answer_id, user_id) VALUES
(1, 'vote reply body', '2025-12-10 12:30:00', 2, 1), -- Voting testing reply
(2, 'delete reply body', '2025-12-11 14:00:00', 2, 3); -- Delete testing reply

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