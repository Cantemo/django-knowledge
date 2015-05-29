#!/bin/bash
export PYTHONPATH='./:../'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#export PYTHONPATH="./$(cd "$( dirname "${BASH_SOURCE[0]}../" )" && cd ../ && pwd )"
echo "Testing Directory: " $DIR
TARGET=$DIR"/manage.py"

#python $TARGET test --pythonpath="../"
python $TARGET test 
