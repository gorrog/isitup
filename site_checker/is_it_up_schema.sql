DROP
TABLE
IF EXISTS
site
CASCADE;

DROP
TABLE
IF EXISTS
error
CASCADE;

CREATE
TABLE
site (
id SERIAL UNIQUE PRIMARY KEY,
url text UNIQUE,
schedule interval,
last_status smallint,
first_checked timestamptz DEFAULT CURRENT_TIMESTAMP
last_checked timestamptz DEFAULT CURRENT_TIMESTAMP
);

CREATE
TABLE
error (
id SERIAL UNIQUE PRIMARY KEY,
site_id integer REFERENCES site (id),
error_timestamp timestamptz DEFAULT CURRENT_TIMESTAMP,
error_code integer
)