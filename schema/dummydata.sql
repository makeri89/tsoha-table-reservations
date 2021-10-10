INSERT INTO users (username, password, isAdmin, isRestaurant) VALUES
  ('admin',
  'pbkdf2:sha256:260000$TAYCMThANt62KMgU$f17955e2e30d9c76a94bb78fccb4ed354eabaa56d9cbaf17e8fdb40dbcbb3962',
  TRUE, FALSE);

INSERT INTO users (first_name, last_name, email, username, password, isAdmin, isRestaurant) VALUES
  ('Test', 'Tester', 'text@example.com', 'tester',
  'pbkdf2:sha256:260000$O7N92e8ker9YRXG5$9f1e07ecec82dbbb4954940edbf1ef6d0f2bb0d9a5bf7a02d6b352a57dd5631d',
  FALSE, TRUE);

INSERT INTO restaurants (name, owner, address, openingHours, serviceTimes) VALUES 
  ('Restaurant Test',
  2, '11 Test Avenue, 00100 Helsinki',
  '{{"mon","12:00","20:00"},
  {"tue","12:00","20:00"},
  {"wed","12:00","20:00"},
  {"thu","12:00","22:00"},
  {"fri","12:00","22:00"},
  {"sat","-","-"},
  {"sun","-","-"}}',
  '{{"mon","12:00", "13:00", "14:00", "17:00", "20:00"},
  {"tue","12:00", "13:00", "14:00", "17:00", "20:00"},
  {"wed","12:00", "13:00", "14:00", "17:00", "20:00"},
  {"thu","12:00", "13:00", "14:00", "18:00", "21:00"},
  {"fri","12:00", "13:00", "14:00", "18:00", "21:00"},
  {"sat","-","-","-","-","-"},
  {"sun","-","-","-","-","-"}}'),
  ('Restaurant Test2',
  2, '22 Test Street, 00200 Helsinki',
  '{{"mon","12:00","16:00"},
  {"tue","12:00","16:00"},
  {"wed","12:00","16:00"},
  {"thu","12:00","22:00"},
  {"fri","12:00","22:00"},
  {"sat","14:00","22:00"},
  {"sun","11:00","16:00"}}',
  '{{"mon","12:00", "13:00", "14:00", "-", "-"},
  {"tue","12:00", "13:00", "14:00", "-", "-"},
  {"wed","12:00", "13:00", "14:00", "-", "-"},
  {"thu","12:00", "13:00", "14:00", "18:00", "21:00"},
  {"fri","12:00", "13:00", "14:00", "18:00", "21:00"},
  {"sat","14:00", "18:00", "21:00", "-", "-"},
  {"sun","11:00","12:00", "13:00", "14:00", "-"}}');

INSERT INTO tables (size, restaurant) VALUES
  (2,1),(2,1),(2,1),(2,1),(4,1),(4,1),
  (2,2),(2,2),(3,2);

INSERT INTO menus (name, restaurant) VALUES ('Lounas', 1),('Lounas', 2);

INSERT INTO menuCourses (course) VALUES ('starter'),('main'),('dessert');

INSERT INTO menuItems (title, price, menu, course) VALUES
  ('Tomaattikeitto', 12, 1, 1),
  ('Burgeri', 18, 1, 2),
  ('Jäätelöannos', 6, 1, 3),
  ('Salaatti', 10, 2, 1),
  ('Pizza', 16, 2, 2);

INSERT INTO reservations (restaurant, guest, date, startTime, pax, createdAt, tableId) VALUES
  (1, 1, TIMESTAMP '2021-10-20', '12:00', 2, NOW(), 1);