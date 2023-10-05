-- public.scores definition
-- Drop table
DROP TABLE public.scores;
CREATE TABLE public.scores (
    id int4 NOT NULL GENERATED ALWAYS AS IDENTITY(
        INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE
    ),
    "date" timestamp NULL DEFAULT now(),
    "user" varchar NULL,
    score int4 NULL,
    CONSTRAINT scores_pkey PRIMARY KEY (id)
);
