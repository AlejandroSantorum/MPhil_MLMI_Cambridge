
fname_res=./results/lstm_dnn_multiple_layers_tri.txt
fname_plot=./imgs/lstm_dnn_multiple_layers_tri.png

limInf=1
jump=1
limSup=3

pracgmmexp=~/MLMI2/pracgmm/exp/FBK_D_A_Z_FlatStart
gmm_triphone_file=xwtri-RO300-TB1000-NM12

# Checking if alignments have been created
ALIGN_DIR="${pracgmmexp}/align-xwtri-hmm84"
if ! [ -d "$ALIGN_DIR" ]; then
    cd ~/MLMI2/pracgmm/exp
    ../tools/steps/step-align $PWD/FBK_D_A_Z_FlatStart/${gmm_triphone_file} hmm84 FBK_D_A_Z_FlatStart/align-xwtri-hmm84
fi

cd ~/MLMI2/pracann/exp

store_folder=LSTM-DNN-MultLayers-Tri
if ! [ -d "$store_folder" ]; then
    mkdir ${store_folder}
fi

if [ "$1" == "-d" ]; then # Deliting previous execution folders if specified
    rm -rf `find ./${store_folder} -name '*LSTM-1L-DNN*'`
    rm -rf $fname_res
fi

# Training and testing multiple hidden layer networks (after one LSTM layer)
for ((n_layers = $limInf; n_layers <= $limSup; n_layers += $jump));
do
    # Training
    ../tools/steps/step-dnntrain -MODELINI ../new_nn_models/lstm/LSTM-1L-DNN-${n_layers}L.FBANK_D_A_Z.ini -GPUID 0 -vvv ../convert/fbk25d/env/environment_D_A_Z $pracgmmexp/align-xwtri-hmm84/align/timit_train.mlf $pracgmmexp/${gmm_triphone_file}/hmm84/MMF $pracgmmexp/${gmm_triphone_file}/hmms.mlist ${store_folder}/LSTM-1L-DNN-${n_layers}L-FBK_D_A_Z/dnntrain
    # Fetching training accuracies: CV set accuracy and train accuracy
    echo "===== Train num_hidden_layers=${n_layers} =====" >> $fname_res
    trainAcc=$(grep 'Train Accuracy' ${store_folder}/LSTM-1L-DNN-${n_layers}L-FBK_D_A_Z/dnntrain/hmm0/LOG | tail -1)
    echo $trainAcc >> $fname_res
    echo "===== Validation num_hidden_layers=${n_layers} =====" >> $fname_res
    cvAcc=$(grep 'Validation Accuracy' ${store_folder}/LSTM-1L-DNN-${n_layers}L-FBK_D_A_Z//dnntrain/hmm0/LOG | tail -1)
    echo $cvAcc >> $fname_res
    # Decoding, i.e., Testing
    ../tools/steps/step-decode -INSWORD -8 -BEAMWIDTH 200 $PWD/${store_folder}/LSTM-1L-DNN-${n_layers}L-FBK_D_A_Z/dnntrain hmm0 ${store_folder}/LSTM-1L-DNN-${n_layers}L-FBK_D_A_Z/decode
    echo "===== Test num_hidden_layers=${n_layers} =====" >> $fname_res
    testAcc=$(grep 'WORD:' ${store_folder}/LSTM-1L-DNN-${n_layers}L-FBK_D_A_Z/decode/test/LOG)
    echo $testAcc >> $fname_res
done

# Plotting results
echo "Plotting results"
xaxis="Number of DNN hidden layers after a LSTM layer"
python3 ./train_cv_test_plot.py $fname_res $fname_plot $xaxis