
\i /opt/pingpong-match/db/init_journal.sql;
\i /opt/pingpong-match/db/init_auth.sql;
\i /opt/pingpong-match/db/init_public.sql;

\COPY auth.group FROM '/opt/pingpong-match/db/csv/auth.group.csv' WITH CSV HEADER;
\COPY auth.user FROM '/opt/pingpong-match/db/csv/auth.user.csv' WITH CSV HEADER;
\COPY auth.user_group FROM '/opt/pingpong-match/db/csv/auth.user_group.csv' WITH CSV HEADER;
\COPY auth.menu FROM '/opt/pingpong-match/db/csv/auth.menu.csv' WITH CSV HEADER;
\COPY auth.group_menu FROM '/opt/pingpong-match/db/csv/auth.group_menu.csv' WITH CSV HEADER;

\i /opt/pingpong-match/db/id_seq_reset.sql;
