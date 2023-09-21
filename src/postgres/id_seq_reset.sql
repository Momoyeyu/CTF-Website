
CREATE OR REPLACE FUNCTION reset_id_seq_tabname(tabname character varying) RETURNS void
  AS $_$
DECLARE
  max_id BIGINT;
BEGIN
  EXECUTE 'SELECT max(id) FROM ' || tabname INTO max_id;
  IF max_id IS NOT NULL THEN
    EXECUTE 'ALTER SEQUENCE ' || tabname || '_id_seq RESTART ' || (max_id+1) ;
  END IF;
END;
$_$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION reset_id_seq() RETURNS integer
  AS $_$
BEGIN

  PERFORM reset_id_seq_tabname('auth.group');
  PERFORM reset_id_seq_tabname('auth.user');
  PERFORM reset_id_seq_tabname('auth.menu');

  RETURN 1;
END;
$_$ LANGUAGE plpgsql;

SELECT reset_id_seq();

-- test
-- select currval('auth.user_id_seq'::regclass);
