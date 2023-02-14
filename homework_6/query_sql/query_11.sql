-- середня оцінка, яку ставить окремий викладач окремому студенту
SELECT t.name AS teacher, s.name AS student, ROUND(AVG(gd.grade), 2) AS avg_grade
FROM grades AS gd
    LEFT JOIN students AS s ON s.id = gd.student_id
    LEFT JOIN disciplines AS d ON d.id = gd.discipline_id
    LEFT JOIN teachers AS t ON t.id = d.teacher_id
WHERE t.id = 1 AND gd.student_id = 13
GROUP BY t.name;
