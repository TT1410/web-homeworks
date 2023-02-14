--список студентів в групі
SELECT g.name AS [group], s.name AS student
FROM groups AS g
    LEFT JOIN students AS s ON s.group_id = g.id
WHERE g.id = 5;