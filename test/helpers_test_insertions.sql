-- COUNTRIES
INSERT INTO countries (country_id, country_name, country_img_url, country_info) VALUES
(1, 'Turkey',  NULL, 'Test country: Turkey'),
(2, 'USA',     NULL, 'Test country: USA'),
(3, 'Germany', NULL, 'Test country: Germany');

-- CITIES
INSERT INTO cities (city_id, city_name, city_img_url, city_info, country_id) VALUES
(1, 'Ankara',        NULL, 'Test city: Ankara',        1),
(2, 'Istanbul',      NULL, 'Test city: Istanbul',      1),
(3, 'New York',      NULL, 'Test city: New York',      2),
(4, 'San Francisco', NULL, 'Test city: San Francisco', 2),
(5, 'Berlin',        NULL, 'Test city: Berlin',        3);

-- USERS
INSERT INTO users (user_id, username, full_name, e_mail_addr, time_created, password, city_id) VALUES
(1, 'alice', 'Alice A', 'alice@test.com', '2025-11-20 09:10:00', 'md5_like_hash_aaaaaaaaaaaaaaa', 1),
(2, 'bob',   'Bob B',   'bob@test.com',   '2025-11-22 11:25:00', 'md5_like_hash_bbbbbbbbbbbbbbb', 2),
(3, 'carol', 'Carol C', 'carol@test.com', '2025-11-28 15:40:00', 'md5_like_hash_cccccccccccccccc', 3),
(4, 'dave',  'Dave D',  'dave@test.com',  '2025-12-01 08:05:00', 'md5_like_hash_dddddddddddddddd', 5),
(5, 'sub_guy', 'mr subscriber', 'subguy@test.com', '2025-12-02 10:00:00', 'md5_like_hash_eeeeeeeeeeeeeee', NULL);

-- CATEGORIES
INSERT INTO categories (category_id, category_label) VALUES
(1, 'Travel'),
(2, 'Food'),
(3, 'Tech'),
(4, 'Study');

-- QUESTIONS
INSERT INTO questions (question_id, time_created, question_title, question_body, user_id, city_id) VALUES
(1, '2025-12-10 10:15:00', 'Best kebab in Istanbul?', 'Looking for kebab places in Istanbul.', 2, 2),
(2, '2025-12-11 14:20:00', 'Where to buy Arduino parts in Ankara?', 'Need Arduino parts in Ankara.',      1, 1),
(3, '2025-12-05 09:05:00', 'Best coworking spaces in NYC?', 'Coworking suggestions in NYC.',          3, 3),
(4, '2025-12-12 18:40:00', 'Golden Gate viewpoints?', 'Best viewpoints around Golden Gate.',         1, 4),
(5, '2025-11-25 12:00:00', 'Study tips for physics?', 'How to study physics effectively?',           4, 5),
(6, '2025-12-13 08:30:00', 'Public transport card for Istanbul?', 'Istanbulkart details?',             2, 2);

-- QUESTION_CATEGORIES
INSERT INTO question_categories (question_id, category_id) VALUES
(1, 1), (1, 2),     -- q1: Travel, Food
(2, 3),             -- q2: Tech
(3, 3), (3, 4),     -- q3: Tech, Study
(4, 1),             -- q4: Travel
(5, 4),             -- q5: Study
(6, 3), (6, 1);     -- q6: Tech, Travel

-- ANSWERS
INSERT INTO answers (answer_id, answer_body, time_created, user_id, question_id) VALUES
(1,  'Try Karadeniz-style kebab spots in Besiktas.', '2025-12-10 12:00:00', 1, 1),
(2,  'Kadikoy has many great options; check reviews.', '2025-12-10 13:00:00', 3, 1),
(3,  'You can find parts at electronics bazaars in Kizilay.', '2025-12-11 16:00:00', 2, 2),
(4,  'Midtown has many coworking options with day passes.', '2025-12-06 10:00:00', 4, 3),
(5,  'Brooklyn coworking spaces are cheaper and nice.', '2025-12-07 11:00:00', 1, 3),
(6,  'Battery Spencer is a classic viewpoint.', '2025-12-12 20:00:00', 3, 4),
(7,  'Get Istanbulkart at metro stations; top up via kiosks.', '2025-12-13 09:00:00', 4, 6),
(8,  'Mobile top-up works; use official app if available.', '2025-12-13 09:10:00', 1, 6),
(9,  'Airport has kiosks; city center is easier.', '2025-12-13 09:20:00', 3, 6),
(10, 'Use spaced repetition + problem solving daily.', '2025-11-26 09:00:00', 2, 5);

-- REPLIES
INSERT INTO replies (reply_id, reply_body, time_created, answer_id, user_id) VALUES
(1, 'Thanks! Any specific place name?', '2025-12-10 12:30:00', 1, 2),
(2, 'Agree, Besiktas is great for food.', '2025-12-10 12:45:00', 1, 3),
(3, 'Nice suggestion, Kadikoy is also crowded though.', '2025-12-10 13:30:00', 2, 1),
(4, 'Do we need a photo for Istanbulkart?', '2025-12-13 09:30:00', 7, 2),
(5, 'No photo needed for standard card.', '2025-12-13 09:35:00', 7, 1),
(6, 'Great, any book recommendation?', '2025-11-26 10:00:00', 10, 4);

-- CITY SUBSCRIPTIONS
INSERT INTO city_subscriptions (city_id, user_id) VALUES
(2, 1), -- user1 -> Istanbul
(4, 1), -- user1 -> San Francisco
(1, 2), -- user2 -> Ankara
(5, 3), -- user3 -> Berlin
(3, 3), -- user3 -> New York
(3, 4); -- user4 -> New York

-- COUNTRY SUBSCRIPTIONS
INSERT INTO country_subscriptions (country_id, user_id) VALUES
(2, 1), -- user1 -> USA
(1, 2), -- user2 -> Turkey
(1, 3), -- user3 -> Turkey
(3, 3), -- user3 -> Germany
(2, 4); -- user4 -> USA

-- QUESTION VOTES (vote_type: 1 up, 0 down)
INSERT INTO question_votes (user_id, question_id, vote_type) VALUES
(1, 1, 1),
(1, 3, 0),
(1, 6, 1),
(2, 2, 1),
(2, 6, 1),
(3, 1, 1),
(3, 4, 1),
(4, 1, 0),
(4, 5, 1);

-- ANSWER VOTES
INSERT INTO answer_votes (user_id, answer_id, vote_type) VALUES
(2, 1, 1),
(3, 1, 0),
(4, 1, 1),
(1, 2, 1),
(2, 2, 0),
(3, 7, 1),
(1, 7, 1),
(2, 7, 1),
(2, 8, 1),
(4, 8, 0),
(1, 9, 1),
(1,10, 0);

-- REPLY VOTES
INSERT INTO reply_votes (user_id, reply_id, vote_type) VALUES
(1, 1, 1),
(3, 1, 1),
(1, 2, 0),
(4, 4, 1),
(3, 5, 1),
(2, 5, 1),
(2, 6, 0);