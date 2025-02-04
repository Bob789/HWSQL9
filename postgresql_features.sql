
--------------------------- PARTITION BY

-- Find the running total of sales for each employee
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    employee_id INT,
    sale_amount NUMERIC
);

INSERT INTO sales (employee_id, sale_amount)
VALUES
    (1, 100),
    (1, 200),
    (2, 150),
    (2, 300),
    (1, 50),
    (2, 100);

SELECT
    employee_id,
    sale_amount,
    SUM(sale_amount) OVER
    (PARTITION BY employee_id ORDER BY id) AS running_total,
    COUNT(*) OVER
    (PARTITION BY employee_id) AS sales_count
FROM sales
where employee_id  = 1
-- with Order by, it counts in a running manner
-- without order by -> aggregate all


-------------------------------------------- JSONB
-- Store and query JSON data
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    details JSONB
);
-- JSON COLUMN == dict { 'key': value ...} JSON
-- <name>itay</name>
-- <color>yello</color>
-- { 'name': 'itay' }
INSERT INTO products (details)
VALUES
    ('{"name": "Laptop", "price": 1200, "features": {"RAM": "16GB", "Storage": "512GB"}}'),
    ('{"name": "Phone", "features": {"RAM": "8GB", "Storage": "256GB"}}');

-- Query specific keys in the JSON
SELECT
    details->>'name' AS product_name,
    details->'features'->>'RAM' AS ram
FROM products;


-------------------------------------------- Arrays
-- Use arrays to store multiple values in a single column
CREATE TABLE array_example (
    id SERIAL PRIMARY KEY,
    numbers INT[]
);

INSERT INTO array_example (numbers)
VALUES
    ('{1, 2, 3}'),
    ('{4}');

-- Query specific array elements
SELECT numbers[1] AS first_element FROM array_example;

-- Search for rows containing a specific number
SELECT * FROM array_example WHERE 3 = ANY(numbers);

-------------------------------------------- GENERATED ALWAYS

-- Automatically calculate column values
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    price NUMERIC,
    tax NUMERIC GENERATED ALWAYS AS (price * 0.2) STORED
);

INSERT INTO products (price) VALUES (100), (200);

-- Tax is automatically calculated
SELECT * FROM products;

----------------- Views
create view get_emp_dept AS
select e.*, d.department_name from employees e
join departments d on e.department_id = d.department_id
order by d.department_name;

----------------- MATERIALIZED Views
create materialized view mat_get_emp_dept AS
select e.*, d.department_name from employees e
join departments d on e.department_id = d.department_id
order by d.department_name;

select * from mat_get_emp_dept ged;

-- only updated after refresh
-- refresh materialized view mat_get_emp_dept;