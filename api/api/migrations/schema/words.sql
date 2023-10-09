-- public.words definition
-- Drop table
DROP TABLE IF EXISTS public.words;
CREATE TABLE public.words (
    id int4 NOT NULL GENERATED ALWAYS AS IDENTITY(
        INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE
    ),
    form_infinitive varchar NOT NULL,
    form_simple_past varchar NOT NULL,
    form_past_participle varchar NOT NULL,
    "translation" varchar NULL,
    difficulty int4 NOT NULL DEFAULT 1,
    CONSTRAINT "PRIMARY_KEY" PRIMARY KEY (id)
);
