
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
CREATE TABLE courses (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    name VARCHAR (32),
    type INTEGER NOT NULL,
    FOREIGN KEY (type) REFERENCES course_types (id)
);
CREATE TABLE course_types (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    descx VARCHAR (32)
);
CREATE TABLE category_course (
    category_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories (id),
    FOREIGN KEY (course_id) REFERENCES courses (id)
);
CREATE TABLE course_student (
    course_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses (id),
    FOREIGN KEY (student_id) REFERENCES students (id)
);
COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
