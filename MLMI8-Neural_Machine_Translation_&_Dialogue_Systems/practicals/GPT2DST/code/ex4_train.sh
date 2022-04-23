#!/bin/bash
#SBATCH -A MLMI-as3159-SL2-GPU
#SBATCH -J mwozdst
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --time=6:00:00
#SBATCH --mail-type=FAIL
#! Uncomment this to prevent the job from being requeued (e.g. if
#! interrupted by node failure or system downtime):
##SBATCH --no-requeue
#SBATCH -p ampere
#! ############################################################
. /etc/profile.d/modules.sh                # Leave this line (enables the module command)
module purge                               # Removes all modules still loaded
module load rhel8/default-amp
module load cuda/11.1 intel/mkl/2017.4
export OMP_NUM_THREADS=1
source /rds/project/rds-xyBFuSj0hm0/MLMI8.L2022/envs/README.MLMI8.GPT2DST.activate

##
JOBID=$SLURM_JOB_ID
LOG=slurm_logs/train-log.$JOBID
ERR=slurm_logs/train-err.$JOBID

mkdir -p slurm_logs/

echo -e "JobID: $JOBID\n======" > $LOG
echo "Time: `date`" >> $LOG
echo "Running on master node: `hostname`" >> $LOG

# CHANGE TRAIN_DATA AND DEV_DATA VARIABLES TO CHANGE MODEL INPUT
TRAIN_DATA=my_data/train_dst.json
DEV_DATA=my_data/dev_dst.json
TRAIN_ARGS=$BDIR/train_arguments.nlu.mwoz21.yaml
#CHECKPOINT=$BDIR/checkpoints/nlu_flat_start/model.60000/

CT=""
if [[ ${CHECKPOINT+x} ]]; then
    CT="--restore $CHECKPOINT"
fi

python $BDIR/train-gpt2-dst.py $CT \
 --train_data $TRAIN_DATA --dev_data $DEV_DATA --args $TRAIN_ARGS -vv >> $LOG 2> $ERR

echo "Time: `date`" >> $LOG
