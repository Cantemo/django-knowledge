#!/bin/bash
export PYTHONPATH="./"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Testing Directory: " $DIR
TARGET=$DIR"/manage.py"

python $TARGET test mock knowledge --pythonpath="../"
