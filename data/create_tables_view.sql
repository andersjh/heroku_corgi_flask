CREATE TABLE "grades" (
	"pet_id"	INTEGER NOT NULL,
	"task_id"	INTEGER NOT NULL,
	"grade"	TEXT,
	"comments"	TEXT,
	PRIMARY KEY("pet_id","task_id")
);

CREATE TABLE "pets" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT,
	"age"	INTEGER,
	"breed"	TEXT,
	"age_adopted"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "training" (
	"id"	INTEGER NOT NULL,
	"task"	TEXT,
	"description"	TEXT,
	PRIMARY KEY("id")
);

CREATE VIEW pet_training as
select g.pet_id, p.name, g.task_id, t.task, g.grade, g.comments 
from pets p
join grades g on g.pet_id = p.id
join training t on t.id =  g.task_id
order by g.pet_id, g.task_id
;