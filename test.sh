#!/bin/sh

set -xe

isort --recursive . -v
flake8 .
