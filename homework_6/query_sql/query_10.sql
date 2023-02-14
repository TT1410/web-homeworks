-- список предметів, які окремому студенту читає окремий викладач
SELECT s.name AS student, t.name AS teacher, d.name AS discipline
FROM grades AS gd
    RIGHT JOIN disciplines AS d ON d.id = gd.discipline_id
    LEFT JOIN teachers AS t ON t.id = d.teacher_id
    LEFT JOIN students AS s ON s.id = gd.student_id
WHERE gd.student_id = 13 AND t.id = 1
GROUP BY d.name;