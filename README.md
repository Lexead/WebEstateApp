# Tasks

##### Task 1

```SELECT s.name AS student, c.name AS course FROM students s LEFT JOIN enrollments e ON s.id=e.student_id LEFT JOIN courses c ON e.course_id=c.id;```

##### Task 2

.env
```PG_DSN="postgresql+driver://username:password@host:port/database"```