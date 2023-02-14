-- студент з найвищим середнім балом з окремого предмета
SELECT
    s.name,
    d.name AS discipline,
    ROUND(AVG(gd.grade), 2) as avg_grade
FROM
    grades AS gd
LEFT JOIN
    students AS s ON s.id = gd.student_id
LEFT JOIN
    disciplines AS d ON d.id = gd.discipline_id
WHERE d.id = 2
GROUP BY s.id, d.id
ORDER BY avg_grade DESC
LIMIT 1;