-- оцінки студента в групі з конкретного предмету
SELECT gp.name AS [group], d.name AS discipline, s.name AS student, gd.created_at, gd.grade
FROM grades AS gd
    LEFT JOIN students AS s ON s.id = gd.student_id
    LEFT JOIN disciplines AS d ON d.id = gd.discipline_id
    LEFT JOIN groups AS gp ON gp.id = s.group_id
WHERE gp.id = 3 AND d.id = 2;