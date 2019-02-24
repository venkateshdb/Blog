

create table posts(
    id integer primary key,
    post_id integer not null,
    title text not null,
    sub_title text not null,
    tags text,
    'timestamp' timestamp
);

create table images(
    post_id integer not null,
    cover_image text,
    body_image text,
)

create table auths(
    'user_id' integer primary key,
    username text not null,
    'password' text not null,
);

create table comments(
    post_id integer not null,
    likes integer,
    comment text,
    views integer
);