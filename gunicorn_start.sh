#!/bin/bash

# Project Name
NAME="estagio"

# Django Project Directory
DJANGODIR=/var/www/projeto_estagio/estagio

# Run gunicorn on the socket file
SOCKFILE=/var/www/projeto_estagio/run/gunicorn.sock

# Gunicorn running as user and group
USER=ubuntu
GROUP=root

# Workers
NUM_WORKERS=3

#Module Setting
#replace hello_django with your project name
DJANGO_SETTINGS_MODULE=estagio.settings
DJANGO_WSGI_MODULE=estagio.wsgi

"gunicorn_start.sh" 44L, 1140C                                                                           1,1           Top

