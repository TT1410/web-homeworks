-- оцінки студентів у певній групі з певного предмета на останньому занятті
SELECT s.name AS student, gp.name AS [group], d.name AS discipline, gd.created_at, gd.grade
FROM grades AS gd
    LEFT JOIN students AS s ON s.id = gd.student_id
    LEFT JOIN disciplines AS d ON d.id = gd.discipline_id
    LEFT JOIN groups AS gp ON gp.id = s.group_id
WHERE d.id = 1
    AND gp.id = 3
    AND gd.created_at = (
        SELECT MAX(gd.created_at)
        FROM grades AS gd
            LEFT JOIN students AS s ON s.id = gd.student_id
            LEFT JOIN groups AS gp ON gp.id = s.group_id
        WHERE gd.discipline_id = 1
            AND gd.id = 3)
ORDER BY gd.created_at DESC;