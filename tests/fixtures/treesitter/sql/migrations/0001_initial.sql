-- Initial schema (PostgreSQL).

-- Accounts of the app.
-- One row per person.
CREATE TABLE IF NOT EXISTS public.users (
    id bigserial PRIMARY KEY,
    email text NOT NULL UNIQUE,
    profile jsonb,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE orders (
    id serial,
    user_id bigint REFERENCES public.users (id),
    total numeric(10, 2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES public.users (id),
    UNIQUE (user_id, id)
);

-- Users with a profile.
CREATE VIEW active_users AS SELECT id, email FROM public.users WHERE profile IS NOT NULL;

-- Totals per user, refreshed nightly.
CREATE MATERIALIZED VIEW order_totals AS SELECT user_id, sum(total) AS total FROM orders GROUP BY user_id;

CREATE INDEX CONCURRENTLY orders_user_idx ON orders (user_id);
