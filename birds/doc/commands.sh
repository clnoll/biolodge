# To delete and recreate the database
dropdb biolodge
createdb biolodge
./manage.py makemigrations
./manage.py migrate

# Load birds
PYTHONPATH=. DJANGO_SETTINGS_MODULE=biolodge.settings python birds/data/read_ebird_csv.py

# Parse ranges (takes hours to complete but adds to db incrementally)
./manage.py birds_parse_ranges

# Compute mpolys from ASTs
./manage.py birds_compute_ranges
