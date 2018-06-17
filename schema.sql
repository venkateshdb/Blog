/*
schema for vlog
*/

create table if not exists post(
    id integer primary key,
    title text not null,
    sub_title text,
    description text not null,
    date text not null,
    tag text not null,
    content text not null,
    image text
);

create table if not exists files(
    name text not null
);

create table if not exists auth(
  id integer primary key ,
  username text not null,
  password text not null
);
