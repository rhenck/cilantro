# Cilantro

Cilantro is a task runner designed to manage long running distributed jobs that
operate on file system objects. It is written in Python (3.6+) and uses
[Celery](http://docs.celeryproject.org/) and [Flask](http://flask.pocoo.org/).

## Quick start

Run these commands in order to run the app in development mode:

    make cp-default-config
    make run

The frontend can then be accessed under http://localhost:7777/.

## Documentation

The documentation is automatically generated when a commit is pushed to the
master branch.
The documentation files are held on the special branch `gh-pages`.

The generated HTML can be viewed via the following URL:

https://dainst.github.io/cilantro/

## Setup development environment

* Copy the `.env-default` file to `.env` and modify it. In most cases only
  `UID` has to be adjusted. The UID / GID of the current user can be read with
  `id -u` / `id -g` on UNIX systems.

* Copy `config/users.yml-default` to `config/users.yml`. This file stores the
  user information and credentials for all available users. In order for the
  tests to be successful it must contain the user `test_user`. This user has
  to be removed in production environments.

  Passwords have to be encrypted with
  [bcrypt](https://en.wikipedia.org/wiki/Bcrypt).

* Install docker (Community Edition)

    You might have to add the proper 3rd party PPA. Refer to the official
    documentation. Example for Ubuntu-based distributions:
    https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce

    `sudo apt install docker-ce`

## Running the app with docker

Dockerfiles for the different services and their dependencies are stored in
the subdirectory `docker/`. The complete stack defined for different
environments is configured with docker-compose files.

To start cilantro for development run:

    make run

To stop the application run:

    make stop

To build and publish the images follow the instructions provided in
[the docker README](docker/README.md).

Published docker images can be found at [dockerhub](https://hub.docker.com/u/dainst/).

### Testing the application manually

In order for the test to function properly you have to create some files with
.tif ending in the folder `./data/staging/foo`.

The web service runs on port 5000. The following command will create a test task:

    curl -XPOST http://localhost:5000/job/test/foo

You can then query the job status with the returned job_id:

    curl http://localhost:5000/job/<job_id>

#### E2E-Tests

Run against current env-configuation (defaults to local cilantro):

    TEST="default" docker-compose up frontend-test

Run against Mock-Backend

    TEST="mock" docker-compose up frontend-test

##### Tips

- change promisesDelay-attribute in  frontend/test/e2e/protractor.conf to slow tests down if you wanna watch them (eg to 150)
- after Testsuite failed look up frontend/e2e/test/screenshots/report.html fpr details

### Monitoring

[Flower](https://flower.readthedocs.io/) is included in the docker config and
is available for debugging under http://localhost:5555.

### Publish Docker Images

To publish a docker image on dockerhub use the buildscript `build.sh` or the
commands in it manually.

Every minor release use the version number as image tag.
This way it is ensured the images are always compatible to the corresponding code.

## Running unit tests

* Start the application as described under [Running the app with docker
](https://github.com/dainst/cilantro#running-the-app-with-docker)

* Run the tests inside the dedicated docker container with the `test/exec_docker_test.sh` script.

*  Alternatively you can run the complete build script out of the
  [build-scripts repository](https://github.com/dainst/build-scripts/).
  After cloning the repo into your workspace, run the following command from within your cilantro directory.

    `../build-scripts/cilantro-build.sh`

This will build, start and stop the docker infrastructure and run the tests.


## Troubleshooting

On Linux hosts the tests will fail because the data directory created by
docker not have the right permissions and the user account that runs the test can not access it. The easiest way to fix that is just to change the owner on the whole directory and subfolders.

    sudo chown -R $(whoami):$(whoami) data/

After that re-run the tests and they may succeed.

## Code style

Cilantro generally uses the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/).

Additionally parameters in method docstrings should be given as follows:

    :param param_type param_name: parameter description
    :raises ErrorType: Exception throw-condition description

### Javascript

- indentation: 4 spaces instead of tab
    - idea: settings->editor->javascript
    - atom: settings->editor
- names
    - for js-variables: camelCase
    - for members of datamodel (dataset, article): under_score
    - in css: snake-case
    - filenames and module names: under_score, eg: myController in my_controller.js
- ES6
    - `let/const` instead of `var` where it makes sense: http://es6-features.org/#BlockScopedVariables
    - arrow function whenever function is not local and [this]-scope is not needed
- more    
    - `===` instead of `==`
    - line endings with `;` even after `}`
    - if without {} only in very simple one liners
