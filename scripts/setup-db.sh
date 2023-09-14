set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "pinesconf" --echo-errors -f /setup-db.sql