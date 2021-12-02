
fname_res=./results/rnn_1layer.txt
fname_plot=./imgs/rnn_1layer.png

limInf=5
jump=5
limSup=25

pracgmmexp=~/MLMI2/pracgmm/exp/MFC_E_D_A_Z_FlatStart

# Checking if alignments have been created
ALIGN_DIR="${pracgmmexp}/align-mono-hmm84"
if ! [ -d "$ALIGN_DIR" ]; then
    cd ~/MLMI2/pracgmm/exp
    ../tools/steps/step-align $PWD/MFC_E_D_A_Z_FlatStart/mono hmm84 MFC_E_D_A_Z_FlatStart/align-mono-hmm84
fi

cd ~/MLMI2/pracann/exp

store_folder=RNN-1L-UnfoldVals
if ! [ -d "$store_folder" ]; then
    mkdir ${store_folder}
fi

if [ "$1" == "-d" ]; then # Deliting previous execution folders if specified
    rm -rf `find ./${store_folder} -name '*RNN-1L*'`
    rm -rf $fname_res
fi

# Training and testing multiple unfold values
for ((unfold_val = $limInf; unfold_val <= $limSup; unfold_val += $jump));
do
    # Modifying file to change unfold value
    python3 ./change_unfold_val.py ../new_nn_models/rnn/RNN-1L.ReLU.MFCC_E_D_A_Z.ini $unfold_val
    # Training
    ../tools/steps/step-dnntrain -MODELINI ../new_nn_models/rnn/RNN-1L.ReLU.MFCC_E_D_A_Z.ini -GPUID 0 -vvv ../convert/mfc13d/env/environment_E_D_A_Z $pracgmmexp/align-mono-hmm84/align/timit_train.mlf $pracgmmexp/mono/hmm84/MMF $pracgmmexp/mono/hmms.mlist ${store_folder}/RNN-1L-MFC_E_D_A_Z-UV${unfold_val}/dnntrain
    # Fetching training accuracies: CV set accuracy and train accuracy
    echo "===== Train unfold_value=${unfold_val} =====" >> $fname_res
    trainAcc=$(grep 'Train Accuracy' ${store_folder}/RNN-1L-MFC_E_D_A_Z-UV${unfold_val}/dnntrain/hmm0/LOG | tail -1)
    echo $trainAcc >> $fname_res
    echo "===== Validation unfold_value=${unfold_val} =====" >> $fname_res
    cvAcc=$(grep 'Validation Accuracy' ${store_folder}/RNN-1L-MFC_E_D_A_Z-UV${unfold_val}/dnntrain/hmm0/LOG | tail -1)
    echo $cvAcc >> $fname_res
    # Decoding, i.e., Testing
    ../tools/steps/step-decode -INSWORD -8 -BEAMWIDTH 200 $PWD/${store_folder}/RNN-1L-MFC_E_D_A_Z-UV${unfold_val}/dnntrain hmm0 ${store_folder}/RNN-1L-MFC_E_D_A_Z-UV${unfold_val}/decode
    echo "===== Test unfold_value=${unfold_val} =====" >> $fname_res
    testAcc=$(grep 'WORD:' ${store_folder}/RNN-1L-MFC_E_D_A_Z-UV${unfold_val}/decode/test/LOG)
    echo $testAcc >> $fname_res
done

# Plotting results
echo "Plotting results"
xaxis="Unfold value"
python3 ./train_cv_test_plot.py $fname_res $fname_plot $xaxis