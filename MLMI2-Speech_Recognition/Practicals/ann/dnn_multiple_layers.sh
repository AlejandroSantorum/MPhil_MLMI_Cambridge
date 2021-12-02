
fname_res=./results/dnn_multiple_layers.txt
fname_plot=./imgs/dnn_multiple_layers.png

limInf=2
jump=1
limSup=9

fixed_contextWidth=5

pracgmmexp=~/MLMI2/pracgmm/exp/MFC_E_D_A_Z_FlatStart

# Checking if alignments have been created
ALIGN_DIR="${pracgmmexp}/align-mono-hmm84"
if ! [ -d "$ALIGN_DIR" ]; then
    cd ~/MLMI2/pracgmm/exp
    ../tools/steps/step-align $PWD/MFC_E_D_A_Z_FlatStart/mono hmm84 MFC_E_D_A_Z_FlatStart/align-mono-hmm84
fi

cd ~/MLMI2/pracann/exp

store_folder=DNN-MultLayers
if ! [ -d "$store_folder" ]; then
    mkdir ${store_folder}
fi

if [ "$1" == "-d" ]; then # Deliting previous execution folders if specified
    rm -rf `find ./${store_folder} -name '*MultH*'`
    rm -rf $fname_res
fi

# Reading results for 1 hidden layer, if they exist
if [ -d ~/MLMI2/pracann/exp/${store_folder}/MH1-MFC_E_D_A_Z-CW${fixed_contextWidth} ]; then
    echo "===== Train num_hidden_layers=1 =====" >> $fname_res
    trainAcc=$(grep 'Train Accuracy' MH1-MFC_E_D_A_Z-CW${fixed_contextWidth}/dnntrain/hmm0/LOG | tail -1)
    echo $trainAcc >> $fname_res
    echo "===== Validation num_hidden_layers=1 =====" >> $fname_res
    cvAcc=$(grep 'Validation Accuracy' MH1-MFC_E_D_A_Z-CW${fixed_contextWidth}/dnntrain/hmm0/LOG | tail -1)
    echo $cvAcc >> $fname_res
    echo "===== Test num_hidden_layers=1 =====" >> $fname_res
    testAcc=$(grep 'WORD:' MH1-MFC_E_D_A_Z-CW${fixed_contextWidth}/decode/test/LOG)
    echo $testAcc >> $fname_res
fi

# Training and testing multiple hidden layer networks
for ((n_layers = $limInf; n_layers <= $limSup; n_layers += $jump));
do
    # Training
    ../tools/steps/step-dnntrain -MODELINI ../new_nn_models/dnn/DNN-${n_layers}L.ReLU.MFCC_E_D_A_Z.ini -GPUID 0 -vvv ../convert/mfc13d/env/environment_E_D_A_Z $pracgmmexp/align-mono-hmm84/align/timit_train.mlf $pracgmmexp/mono/hmm84/MMF $pracgmmexp/mono/hmms.mlist ${store_folder}/MultH${n_layers}-MFC_E_D_A_Z-CW${fixed_contextWidth}/dnntrain
    # Fetching training accuracies: CV set accuracy and train accuracy
    echo "===== Train num_hidden_layers=${n_layers} =====" >> $fname_res
    trainAcc=$(grep 'Train Accuracy' ${store_folder}/MultH${n_layers}-MFC_E_D_A_Z-CW${fixed_contextWidth}/dnntrain/hmm0/LOG | tail -1)
    echo $trainAcc >> $fname_res
    echo "===== Validation num_hidden_layers=${n_layers} =====" >> $fname_res
    cvAcc=$(grep 'Validation Accuracy' ${store_folder}/MultH${n_layers}-MFC_E_D_A_Z-CW${fixed_contextWidth}/dnntrain/hmm0/LOG | tail -1)
    echo $cvAcc >> $fname_res
    # Decoding, i.e., Testing
    ../tools/steps/step-decode -INSWORD -8 -BEAMWIDTH 200 $PWD/${store_folder}/MultH${n_layers}-MFC_E_D_A_Z-CW${fixed_contextWidth}/dnntrain hmm0 ${store_folder}/MultH${n_layers}-MFC_E_D_A_Z-CW${fixed_contextWidth}/decode
    echo "===== Test num_hidden_layers=${n_layers} =====" >> $fname_res
    testAcc=$(grep 'WORD:' ${store_folder}/MultH${n_layers}-MFC_E_D_A_Z-CW${fixed_contextWidth}/decode/test/LOG)
    echo $testAcc >> $fname_res
done

# Plotting results
echo "Plotting results"
xaxis="Number of hidden layers"
python3 ./train_cv_test_plot.py $fname_res $fname_plot $xaxis