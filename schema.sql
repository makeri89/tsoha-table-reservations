CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  email TEXT,
  username TEXT,
  password TEXT,
  isAdmin BOOLEAN,
  isRestaurant BOOLEAN
);

CREATE TABLE IF NOT EXISTS restaurants (
  id SERIAL PRIMARY KEY,
  name TEXT,
  owner INTEGER REFERENCES users,
  address TEXT
);

CREATE TABLE IF NOT EXISTS tables (
  id SERIAL PRIMARY KEY,
  size INTEGER,
  restaurant INTEGER REFERENCES restaurants
);

CREATE TABLE IF NOT EXISTS menus (
  id SERIAL PRIMARY KEY,
  restaurant INTEGER REFERENCES restaurants
);

CREATE TABLE IF NOT EXISTS menuCourses (
  id SERIAL PRIMARY KEY,
  course TEXT
);

CREATE TABLE IF NOT EXISTS menuItems (
  id SERIAL PRIMARY KEY,
  title TEXT,
  description TEXT,
  price INTEGER,
  menu INTEGER REFERENCES menus,
  course INTEGER REFERENCES menuCourses
);

CREATE TABLE IF NOT EXISTS reservations (
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

CREATE TABLE IF NOT EXISTS reviews (
  id SERIAL PRIMARY KEY,
  restaurant INTEGER REFERENCES restaurants,
  guest INTEGER REFERENCES users,
  stars INTEGER,
  review TEXT,
  createdAt TIMESTAMP
);