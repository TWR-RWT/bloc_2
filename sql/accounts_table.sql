CREATE TABLE accounts (
    user_id serial primary key,
    username character varying(50) NOT NULL,
    password character varying(100) NOT NULL,
    role character varying(50) NOT NULL
);
