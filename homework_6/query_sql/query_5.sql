-- які предмети викладає певний викладач
SELECT t.name AS teacher, d.name AS discipline
FROM disciplines AS d
    LEFT JOIN teachers AS t ON t.id = d.teacher_id
WHERE t.id = 3
ORDER BY d.name;