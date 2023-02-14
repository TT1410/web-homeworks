-- середній бал на потоці
SELECT ROUND(AVG(g.grade), 2) AS avg_grade
FROM grades AS g;
