ON UPDATE CASCADE ,ON DELETE SET NULL ,ON DELETE CASCADE

-- REPLACE statement in SQL
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);
REPLACE INTO students (id, name, age)
VALUES (1, 'Alice', 20);
Important Notes:
REPLACE deletes the existing row before inserting the new one, which means it may cause auto-increment IDs to skip values.
It only works when a PRIMARY KEY or UNIQUE INDEX is defined on the table.
If no existing row matches the primary key, REPLACE behaves like INSERT.
----------*
What is UPSERT in SQL?
UPSERT (a combination of "UPDATE" and "INSERT") is a SQL operation that inserts a new row if it does not exist, or updates an existing row if it does. This is useful for preventing duplicate data while ensuring existing records remain updated.

Different SQL databases handle UPSERT differently:

1. MySQL: Using INSERT ... ON DUPLICATE KEY UPDATE
In MySQL, you can use INSERT ... ON DUPLICATE KEY UPDATE:

CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);

INSERT INTO students (id, name, age)
VALUES (1, 'Alice', 20)
ON DUPLICATE KEY UPDATE name = VALUES(name), age = VALUES(age);

In PostgreSQL

INSERT INTO students (id, name, age)
VALUES (1, 'Alice', 20)
ON CONFLICT (id)
DO UPDATE SET name = EXCLUDED.name, age = EXCLUDED.age;

If id = 1 does not exist, it inserts the new row.
If id = 1 already exists, it updates the name and age columns.

----------*

Using DISTINCT in PostgreSQL

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    grade VARCHAR(10)
);

INSERT INTO students (name, age, grade) VALUES
('Alice', 20, 'A'),
('Bob', 21, 'B'),
('Alice', 20, 'A'),
('Charlie', 22, 'A'),
('Bob', 21, 'B'),
('David', 23, 'C');

SELECT DISTINCT name FROM students;

Output
 name
--------
 Alice
 Bob
 Charlie
 David
(4 rows)

-----------*

Using GROUP BY with HAVING in PostgreSQL

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    grade VARCHAR(10)
);

INSERT INTO students (name, age, grade) VALUES
('Alice', 20, 'A'),
('Bob', 21, 'B'),
('Charlie', 22, 'A'),
('David', 23, 'C'),
('Eve', 22, 'B'),
('Frank', 20, 'A'),
('Grace', 21, 'C'),
('Helen', 22, 'A'),
('Isaac', 23, 'B');

We want to count students in each grade but only show grades with more than 2 students.

SELECT grade, COUNT(*) AS student_count
FROM students
GROUP BY grade
HAVING COUNT(*) > 2;

 grade | student_count
-------+--------------
 A     | 4
 B     | 3
(2 rows)

-----------*

How to Rename a Table
Let's say we have a table named students that we want to rename to pupils:

ALTER TABLE students RENAME TO pupils;

-----------*
Renaming a Column in a Table
If you want to rename a column inside a table, use:

ALTER TABLE pupils RENAME COLUMN name TO full_name;

-----------*

How to Add a New Column to a Table
Let's say we have a table called students and we want to add a column for the student's email.

ALTER TABLE students ADD COLUMN email VARCHAR(100);
ALTER TABLE students ADD COLUMN status VARCHAR(10) DEFAULT 'active';
ALTER TABLE students ADD COLUMN age INT NOT NULL;

Adding a Column with a CHECK Constraint
ALTER TABLE students ADD COLUMN grade CHAR(1) CHECK (grade IN ('A', 'B', 'C', 'D', 'F'));

-----------*

Generated Column (Auto-Calculated Column) in PostgreSQL

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    product VARCHAR(50),
    quantity INT,
    price NUMERIC(10,2),
);

INSERT INTO orders (product, quantity, price) VALUES
('Laptop', 2, 1200.50),
('Phone', 3, 799.99);

SELECT
    id,
    product,
    quantity,
    price,
    CAST(quantity * price AS NUMERIC(10,2)) AS total_price
FROM orders;


 id | product | quantity | price   | total_price
----+---------+----------+---------+------------
  1 | Laptop  | 2        | 1200.50 | 2401.00
  2 | Phone   | 3        | 799.99  | 2399.97






