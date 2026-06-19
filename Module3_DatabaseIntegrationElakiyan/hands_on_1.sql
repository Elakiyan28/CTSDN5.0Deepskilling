
-- Task 1: Create Database & Tables


CREATE DATABASE college_db;
USE college_db;

-- Departments table
CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    head_of_dept VARCHAR(100),
    budget DECIMAL(12,2)
);

-- Students table
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Courses table
CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,
    max_seats INT DEFAULT 60,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Enrollments table
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL)
);

-- Professors table
CREATE TABLE professors (
    professor_id INT PRIMARY KEY AUTO_INCREMENT,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);


-- Task 2: Normalisation Analysis


-- 1NF: All columns hold atomic values (no multi-valued fields).
-- 2NF: In enrollments, every non-key column depends fully on (student_id, course_id).
-- 3NF: No transitive dependencies (dept_name stored only in departments, not students).

-- Task 3: Alter & Extend Schema


-- Add column phone_number to students
ALTER TABLE students ADD COLUMN phone_number VARCHAR(15);

-- Rename hod_name to head_of_dept (already applied above)
-- ALTER TABLE departments CHANGE hod_name head_of_dept VARCHAR(100);

-- Drop phone_number (simulate rollback)
ALTER TABLE students DROP COLUMN phone_number;
