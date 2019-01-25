#!/bin/sh
set -e

cd doc

# Generate rst files from sources
sphinx-apidoc -o . ../

# Python modules are imported for reading the docstrings, therefore some
# environment variables are needed
BROKER_HOST=broker BROKER_USER=user BROKER_PASSWORD=password \
DB_HOST=db \
CONFIG_DIR=../config TEST_RESOURCE_DIR=test/resources WORKING_DIR=/data/workspace \
REPOSITORY_DIR=/data/repository STAGING_DIR=/data/staging \
OJS_SERVER=ojs OJS_PORT=80 OJS_PATH=ojs OJS_AUTH_KEY=YWRtaW4=:cGFzc3dvcmQ= \
JOB_DB_URL=localhost JOB_DB_PORT=27017 JOB_DB_NAME=job_database \
make html

# # cleanup
# rm -r doc/_build/doctrees
#
# find doc -maxdepth 1 -type f \
# ! -name 'api.rst' ! -name 'build-doc.sh' \! -name 'conf.py' \
# ! -name 'index.rst' ! -name 'Makefile' ! -name 'requirements.txt' \
# -exec rm -f {} +
