-- середня оцінка, яку ставить конкретний викладач зі своїх предметів
SELECT t.name AS teacher, ROUND(AVG(gd.grade), 2) AS avg_grade
FROM grades AS gd
    LEFT JOIN disciplines AS d ON d.id = gd.discipline_id
    LEFT JOIN teachers AS t ON t.id = d.teacher_id
WHERE t.id = 3
GROUP BY t.name;
