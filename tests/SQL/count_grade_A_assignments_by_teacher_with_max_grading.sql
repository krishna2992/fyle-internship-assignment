WITH TempTable AS (
    select teacher_id , count(*) as tea_count FROM assignments
    where state = 'GRADED'
    GROUP BY teacher_id
)

SELECT count(*) from assignments 
where teacher_id = ( select teacher_id from Temptable 
                     order by  tea_count 
                     DESC LIMIT 1)
and state = 'GRADED'
and grade = 'A';