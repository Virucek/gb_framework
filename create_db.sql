
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS course_types;
DROP TABLE IF EXISTS category_course;
DROP TABLE IF EXISTS course_student;

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (32)
);
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (32),
    parent_category INTEGER
);

-- ВНЕСТИ В ОДНУ ТАБЛИЦУ С УКАЗАНИЕМ ТИПА? - В ДАННЫЙ МОМЕНТ, ОНИ ОДИНАКОВЫ
CREATE TABLE courses (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    name VARCHAR (32),
    type VARCHAR (32),
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories (id)
--    type INTEGER NOT NULL,
--    FOREIGN KEY (type) REFERENCES course_types (id)
);
-- CREATE TABLE course_types (
--    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
--    descx VARCHAR (32)
--);

-- ВНЕСТИ В ОДНУ ТАБЛИЦУ С УКАЗАНИЕМ ТИПА?
--CREATE TABLE online_courses (
--    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
--    name VARCHAR (32),
--    category_id INTEGER,
--    FOREIGN KEY (category_id) REFERENCES categories (id)
--);
--
--CREATE TABLE offline_courses (
--    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
--    name VARCHAR (32),
--    category_id INTEGER,
--    FOREIGN KEY (category_id) REFERENCES categories (id)
--);

-- КУРСЫ МОГУТ БЫТЬ В РАЗНЫХ КАТЕГОРИЯХ (?)
--CREATE TABLE category_course (
--    category_id INTEGER NOT NULL,
--    course_id INTEGER NOT NULL,
--    FOREIGN KEY (category_id) REFERENCES categories (id),
--    FOREIGN KEY (course_id) REFERENCES courses (id)
--);
CREATE TABLE course_student (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    course_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses (id),
    FOREIGN KEY (student_id) REFERENCES students (id)
);
COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
