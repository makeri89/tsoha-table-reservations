CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  email TEXT,
  username TEXT,
  password TEXT,
  isAdmin BOOLEAN,
  isRestaurant BOOLEAN
);

CREATE TABLE restaurants (
  id SERIAL PRIMARY KEY,
  name TEXT,
  owner INTEGER REFERENCES users,
  address TEXT
);

CREATE TABLE tables (
  id SERIAL PRIMARY KEY,
  size INTEGER,
  restaurant INTEGER REFERENCES restaurants
);

CREATE TABLE menus (
  id SERIAL PRIMARY KEY,
  restaurant INTEGER REFERENCES restaurants
);

CREATE TABLE menuCourses (
  id SERIAL PRIMARY KEY,
  course TEXT
);

CREATE TABLE menuItems (
  id SERIAL PRIMARY KEY,
  title TEXT,
  description TEXT,
  price INTEGER,
  menu INTEGER REFERENCES menus,
  course INTEGER REFERENCES menuCourses
);

CREATE TABLE reservations (
  id SERIAL PRIMARY KEY,
  restaurant INTEGER REFERENCES restaurants,
  guest INTEGER REFERENCES users,
  date TEXT,
  startTime TEXT,
  pax INTEGER,
  allergies TEXT,
  wishes TEXT,
  createdAt TIMESTAMP
);

CREATE TABLE reviews (
  id SERIAL PRIMARY KEY,
  restaurant INTEGER REFERENCES restaurants,
  guest INTEGER REFERENCES users,
  review TEXT,
  createdAt TIMESTAMP
);