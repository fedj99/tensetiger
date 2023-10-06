-- public.users definition
-- Drop table
DROP TABLE public.users;
CREATE TABLE public.users (
    id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
    username varchar NOT NULL,
    last_logon timestamp NULL,
    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT users_un UNIQUE (username)
);
