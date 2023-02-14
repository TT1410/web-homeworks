-- 5 студентів з найбільшим середнім балом з усіх предметів
SELECT
    s.name,
    gp.name,
    ROUND(AVG(gd.grade), 2) as avg_grade
FROM
    students AS s
LEFT JOIN
    groups AS gp ON s.group_id = gp.id
LEFT JOIN
    grades AS gd ON s.id = gd.student_id
GROUP BY s.name
ORDER BY avg_grade DESC
LIMIT 5;
