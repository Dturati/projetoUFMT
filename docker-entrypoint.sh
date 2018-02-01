#!/bin/bash
python manage.py migrate        # Apply database migrations
python manage.py collectstatic --clear --noinput # clearstatic files
python manage.py collectstatic --noinput  # collect static files
# Prepare log files and start outputting logs to stdout
touch /logs/gunicorn.log
touch /logs/access.log
tail -n 0 -f /srv/logs/*.log &
echo Starting nginx
# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn estagio.wsgi:application \
    --name estagio \
    --bind unix:estagio.sock \
    --workers 3 \
    --log-level=info \
    --log-file=/logs/gunicorn.log \
    --access-logfile=/logs/access.log &
exec service nginx start

