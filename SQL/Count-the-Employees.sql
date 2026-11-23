-- HackerRank SQL: Count the Employees
--
-- COMPANY(ID, NAME, EMPLOYEES). Print the IDs of companies with more than
-- 10000 employees, ordered by ID.
--
-- SQL works in this order, not in the order it is written:
--   FROM COMPANY             take every row of the table
--   WHERE EMPLOYEES > 10000  keep the rows that pass ("more than" is >, not >=)
--   SELECT ID                keep only the ID column of those rows
--   ORDER BY ID              sort the result; without it the row order is not guaranteed
SELECT ID
FROM COMPANY
WHERE EMPLOYEES > 10000
ORDER BY ID;
