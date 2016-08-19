DROP
TABLE
IF EXISTS
url
CASCADE;

DROP
TABLE
IF EXISTS
error
CASCADE;

CREATE
TABLE
url (
id SERIAL UNIQUE PRIMARY KEY,
url text UNIQUE,
schedule interval,
last_status smallint,
last_checked timestamptz DEFAULT CURRENT_TIMESTAMP
);

CREATE
TABLE
error (
id SERIAL UNIQUE PRIMARY KEY,
url_id integer REFERENCES url (id),
error_timestamp timestamptz DEFAULT CURRENT_TIMESTAMP,
error_code integer
)