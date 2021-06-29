#!/bin/bash

# first wait for elasticsearch to be ready and create database schema, then run
# server with uwsgi

python3 runIt.py
uwsgi uwsgi.ini
