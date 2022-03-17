#!/bin/bash

# Environment to run jupyter notebooks
NOTEBOOK_PORT=8087
if [ "$1" == "-nb" ]; then
    module purge
    module load python-3.6.1-gcc-5.4.0-64u3a4w
    module load anaconda/3.2019-10
    eval "$(conda shell.bash hook)"
    conda activate /home/$USER/envs/MLMI8.openfst
    export PYTHONPATH=/home/$USER/envs/MLMI8.openfst/lib/python3.6/site-packages/openfst_python:$PYTHONPATH

    jupyter notebook --no-browser --ip=127.0.0.1 --port=$NOTEBOOK_PORT

# Environment to run the majority of the practical
else
    source /rds/project/rds-xyBFuSj0hm0/MLMI8.L2022/envs/README.MLMI8.1.activate
fi

GDBNMTBDIR=/rds/project/rds-xyBFuSj0hm0/MLMI8.L2022/GDBNMT/
