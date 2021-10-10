CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  email TEXT UNIQUE,
  username TEXT UNIQUE,
  password TEXT,
  isAdmin BOOLEAN,
  isRestaurant BOOLEAN
);

CREATE TABLE IF NOT EXISTS restaurants (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE,
  owner INTEGER REFERENCES users ON DELETE CASCADE,
  address TEXT,
  openingHours TEXT[][],
  serviceTimes TEXT[][]
);

CREATE TABLE IF NOT EXISTS tables (
  id SERIAL PRIMARY KEY,
  size INTEGER,
  restaurant INTEGER REFERENCES restaurants ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS menus (
  id SERIAL PRIMARY KEY,
  name TEXT,
  restaurant INTEGER REFERENCES restaurants ON DELETE CASCADE
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
  menu INTEGER REFERENCES menus ON DELETE CASCADE,
  course INTEGER REFERENCES menuCourses ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reservations (
  id SERIAL PRIMARY KEY,
  restaurant INTEGER REFERENCES restaurants ON DELETE CASCADE,
  guest INTEGER REFERENCES users ON DELETE CASCADE,
  date TIMESTAMP,
  startTime TEXT,
  pax INTEGER,
  allergies TEXT,
  wishes TEXT,
  createdAt TIMESTAMP,
  tableId INTEGER REFERENCES tables ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reviews (
  id SERIAL PRIMARY KEY,
  restaurant INTEGER REFERENCES restaurants ON DELETE CASCADE,
  guest INTEGER REFERENCES users ON DELETE CASCADE,
  stars INTEGER,
  review TEXT,
  createdAt TIMESTAMP
);
