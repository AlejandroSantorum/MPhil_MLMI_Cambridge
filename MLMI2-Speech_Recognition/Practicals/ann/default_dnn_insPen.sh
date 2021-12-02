### Decoding with different insertion penalties
limInf=-30
jump=5
limSup=30

fname_res=./results/defaultANN_insPen.txt
fname_plot=./imgs/defaultANN_insPen.png

train_mfc=MF0-MFC
train_fbk=MF0-FBK

if [ "$1" == "-d" ]; then # Deliting previous execution folders if specified
    rm -rf `find ./${train_mfc} -name '*decode-insPen*'`
    rm -rf `find ./${train_fbk} -name '*decode-insPen*'`
    rm -rf $fname_res
fi

################################################################
#### MFFCs

### Checking if alignments have been created
param_mfc=MFC_E_D_A_Z_FlatStart
ALIGN_DIR="~/MLMI2/pracgmm/exp/${param_mfc}/align-mono-hmm84"
if ! [ -d "$ALIGN_DIR" ]; then
    cd ~/MLMI2/pracgmm/exp
    ../tools/steps/step-align $PWD/${param_mfc}/mono hmm84 ${param_mfc}/align-mono-hmm84
fi

cd ~/MLMI2/pracann/exp

### Checking if training has been executed
TRAIN_DIR="~/MLMI2/pracann/exp/${train_mfc}/dnntrain"
if ! [ -d "$TRAIN_DIR" ]; then
    pracgmmexp_mfc=~/MLMI2/pracgmm/exp/${param_mfc}
    ../tools/steps/step-dnntrain -GPUID 0 -vvv ../convert/mfc13d/env/environment_E_D_A_Z $pracgmmexp_mfc/align-mono-hmm84/align/timit_train.mlf $pracgmmexp_mfc/mono/hmm84/MMF $pracgmmexp_mfc/mono/hmms.mlist ${train_mfc}/dnntrain
fi

for ((inspen = $limInf; inspen <= $limSup; inspen += $jump));
do
    # Executing decoding (testing)
    ../tools/steps/step-decode -INSWORD ${inspen} -CORETEST -BEAMWIDTH 200 $PWD/${train_mfc}/dnntrain hmm0 ${train_mfc}/decode-insPen${inspen}
    # Fetching data
    echo "===== DefaultANN_MFC_E_D_A_Z_FlatStart insertionPenalty=${inspen} =====" >> $fname_res
    resSent=$(grep 'SENT:' ${train_mfc}/decode-insPen${inspen}/test/LOG)
    echo $resSent >> $fname_res
    resWord=$(grep 'WORD:' ${train_mfc}/decode-insPen${inspen}/test/LOG)
    echo $resWord >> $fname_res
done


################################################################
#### FBK

### Checking if alignments have been created
param_fbk=FBK_D_A_Z_FlatStart
ALIGN_DIR="~/MLMI2/pracgmm/exp/${param_fbk}/align-mono-hmm84"
if ! [ -d "$ALIGN_DIR" ]; then
    cd ~/MLMI2/pracgmm/exp
    ../tools/steps/step-align $PWD/${param_fbk}/mono hmm84 ${param_fbk}/align-mono-hmm84
fi

cd ~/MLMI2/pracann/exp

### Checking if training has been executed
TRAIN_DIR="~/MLMI2/pracann/exp/${train_fbk}/dnntrain"
if ! [ -d "$TRAIN_DIR" ]; then
    pracgmmexp_fbk=~/MLMI2/pracgmm/exp/${param_fbk}
    ../tools/steps/step-dnntrain -GPUID 0 -vvv ../convert/fbk25d/env/environment_D_A_Z $pracgmmexp_fbk/align-mono-hmm84/align/timit_train.mlf $pracgmmexp_fbk/mono/hmm84/MMF $pracgmmexp_fbk/mono/hmms.mlist ${train_fbk}/dnntrain
fi

for ((inspen = $limInf; inspen <= $limSup; inspen += $jump));
do
    # Executing decoding (testing)
    ../tools/steps/step-decode -INSWORD ${inspen} -CORETEST -BEAMWIDTH 200 $PWD/${train_fbk}/dnntrain hmm0 ${train_fbk}/decode-insPen${inspen}
    # Fetching data
    echo "===== DefaultANN_FBK_D_A_Z_FlatStart insertionPenalty=${inspen} =====" >> $fname_res
    resSent=$(grep 'SENT:' ${train_fbk}/decode-insPen${inspen}/test/LOG)
    echo $resSent >> $fname_res
    resWord=$(grep 'WORD:' ${train_fbk}/decode-insPen${inspen}/test/LOG)
    echo $resWord >> $fname_res
done


# Plotting results
xaxis="Insertion Penalty"
echo "Plotting Defaul ANN insertion penaly tuning results"
python3 ./monophone_plots.py $fname_res $fname_plot $xaxis
