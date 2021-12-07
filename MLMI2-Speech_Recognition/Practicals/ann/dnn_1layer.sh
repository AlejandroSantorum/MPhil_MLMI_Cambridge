
fname_res=./results/dnn_1layer.txt
fname_plot=./imgs/dnn_1layer.png

limInf=1
jump=2
limSup=11

cd ~/MLMI2/pracann/exp

store_folder=DNN-1Layer
if ! [ -d "$store_folder" ]; then
    mkdir ${store_folder}
fi

if [ "$1" == "-d" ]; then # Deliting previous execution folders if specified
    rm -rf `find ./${store_folder} -name '*MH1*'`
    rm -rf $fname_res
fi

######### MFCCs #########
cd ~/MLMI2/pracann/exp
for param in _E_Z _E_D_A_Z
do
    # Checking if alignments have been created
    pracgmmexp_mfc=~/MLMI2/pracgmm/exp/MFC${param}_FlatStart
    ALIGN_DIR="${pracgmmexp_mfc}/align-mono-hmm84"
    if ! [ -d "$ALIGN_DIR" ]; then
        cd ~/MLMI2/pracgmm/exp
        ../tools/steps/step-align $PWD/MFC${param}_FlatStart/mono hmm84 MFC${param}_FlatStart/align-mono-hmm84
        cd ~/MLMI2/pracann/exp
    fi
    for ((context_width = $limInf; context_width <= $limSup; context_width += $jump));
    do
        # Modifying file to change context shift
        python3 ./change_context_width.py ../new_nn_models/dnn/DNN-1L.ReLU.MFCC${param}.ini $context_width
        # Training
        ../tools/steps/step-dnntrain -MODELINI ../new_nn_models/dnn/DNN-1L.ReLU.MFCC${param}.ini -GPUID 0 -vvv ../convert/mfc13d/env/environment${param} $pracgmmexp_mfc/align-mono-hmm84/align/timit_train.mlf $pracgmmexp_mfc/mono/hmm84/MMF $pracgmmexp_mfc/mono/hmms.mlist ${store_folder}/MH1-MFC${param}-CW${context_width}/dnntrain
        # Fetching training accuracies: CV set accuracy and train accuracy
        echo "===== DNN1L_MFC${param}_FlatStart Train contextWidth=${context_width} =====" >> $fname_res
        trainAcc=$(grep 'Train Accuracy' ${store_folder}/MH1-MFC${param}-CW${context_width}/dnntrain/hmm0/LOG | tail -1)
        echo $trainAcc >> $fname_res
        echo "===== DNN1L_MFC${param}_FlatStart CV contextWidth=${context_width} =====" >> $fname_res
        cvAcc=$(grep 'Validation Accuracy' ${store_folder}/MH1-MFC${param}-CW${context_width}/dnntrain/hmm0/LOG | tail -1)
        echo $cvAcc >> $fname_res
        # Decoding, i.e., Testing
        ../tools/steps/step-decode -INSWORD -8 -BEAMWIDTH 200 $PWD/${store_folder}/MH1-MFC${param}-CW${context_width}/dnntrain hmm0 ${store_folder}/MH1-MFC${param}-CW${context_width}/decode
        echo "===== DNN1L_MFC${param}_FlatStart Test contextWidth=${context_width} =====" >> $fname_res
        testAcc=$(grep 'WORD:' ${store_folder}/MH1-MFC${param}-CW${context_width}/decode/test/LOG | tail -1)
        echo $testAcc >> $fname_res
    done
done

######### Filter Bank #########
cd ~/MLMI2/pracann/exp
for param in _Z _D_A_Z
do
    # Checking if alignments have been created
    pracgmmexp_fbk=~/MLMI2/pracgmm/exp/FBK${param}_FlatStart
    ALIGN_DIR="${pracgmmexp_fbk}/align-mono-hmm84"
    if ! [ -d "$ALIGN_DIR" ]; then
        cd ~/MLMI2/pracgmm/exp
        ../tools/steps/step-align $PWD/FBK${param}_FlatStart/mono hmm84 FBK${param}_FlatStart/align-mono-hmm84
        cd ~/MLMI2/pracann/exp
    fi
    for ((context_width = $limInf; context_width <= $limSup; context_width += $jump));
    do
        # Modifying file to change context shift
        python3 ./change_context_width.py ../new_nn_models/dnn/DNN-1L.ReLU.FBANK${param}.ini $context_width
        # Training
        ../tools/steps/step-dnntrain -MODELINI ../new_nn_models/dnn/DNN-1L.ReLU.FBANK${param}.ini -GPUID 0 -vvv ../convert/fbk25d/env/environment${param} $pracgmmexp_fbk/align-mono-hmm84/align/timit_train.mlf $pracgmmexp_fbk/mono/hmm84/MMF $pracgmmexp_fbk/mono/hmms.mlist ${store_folder}/MH1-FBK${param}-CW${context_width}/dnntrain
        # Fetching training accuracies: CV set accuracy and train accuracy
        echo "===== DNN1L_FBK${param}_FlatStart Train contextWidth=${context_width} =====" >> $fname_res
        trainAcc=$(grep 'Train Accuracy' ${store_folder}/MH1-FBK${param}-CW${context_width}/dnntrain/hmm0/LOG | tail -1)
        echo $trainAcc >> $fname_res
        echo "===== DNN1L_FBK${param}_FlatStart CV contextWidth=${context_width} =====" >> $fname_res
        cvAcc=$(grep 'Validation Accuracy' ${store_folder}/MH1-FBK${param}-CW${context_width}/dnntrain/hmm0/LOG | tail -1)
        echo $cvAcc >> $fname_res
        # Decoding, i.e., Testing
        ../tools/steps/step-decode -INSWORD -8 -BEAMWIDTH 200 $PWD/${store_folder}/MH1-FBK${param}-CW${context_width}/dnntrain hmm0 ${store_folder}/MH1-FBK${param}-CW${context_width}/decode
        echo "===== DNN1L_FBK${param}_FlatStart Test contextWidth=${context_width} =====" >> $fname_res
        testAcc=$(grep 'WORD:' ${store_folder}/MH1-FBK${param}-CW${context_width}/decode/test/LOG | tail -1)
        echo $testAcc >> $fname_res
    done
done

# Plotting results
echo "Plotting results"
xaxis="Context window width"
python3 ./mult_models_TCVT_plot.py $fname_res $fname_plot $xaxis