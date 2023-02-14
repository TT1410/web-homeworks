-- список предметів, на які ходить студент
SELECT s.name AS student, d.name as discipline
FROM grades AS gd
    LEFT JOIN students AS s ON s.id = gd.student_id
    LEFT JOIN disciplines AS d ON d.id = gd.discipline_id
WHERE gd.student_id = 2
GROUP BY discipline;