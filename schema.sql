drop table if exists flashcard;
create table flashcard (
  id integer primary key autoincrement,
  front string not null,
  back string not null
);
