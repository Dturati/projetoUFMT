# Project Name
NAME="estagio"

# Django Project Directory
DJANGODIR=/home/david/Documentos/projeto_estagio_django/estagio

# Run gunicorn on the socket file
SOCKFILE=/home/david/Documentos/projeto_estagio_django/run/gunicorn.sock

# Gunicorn running as user and group
USER=ubuntu
GROUP=root

# Workers
NUM_WORKERS=3

#Module Setting
#replace hello_django with your project name
DJANGO_SETTINGS_MODULE=estagio.settings
DJANGO_WSGI_MODULE=estagio.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/david/Documentos/projeto_estagio_django/env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/david/Documentos/projeto_estagio_django/env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER --group=$GROUP \
--bind=unix:$SOCKFILE \
--log-level=debug \
--log-file=-
                 
