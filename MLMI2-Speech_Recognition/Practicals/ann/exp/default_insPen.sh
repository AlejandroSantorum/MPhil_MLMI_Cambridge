
limInf=-30
jump=5
limSup=30

fname_res=./results/defaultANN_insPen.txt
fname_plot=./imgs/defaultANN_insPen.png
for ((inspen = $limInf; inspen <= limSup; inspen += jump));
do
    # Executing decoding (testing)
    ../tools/steps/step-decode -INSWORD ${inspen} -CORETEST -BEAMWIDTH 200 $PWD/MH0/dnntrain hmm0 MH0/decode-insPen${inspen}
    # Fetching data
    echo "===== DefaultANN_MFC_E_D_A_Z_FlatStart insertionPenalty=${inspen} =====" >> $fname_res
    resSent=$(grep 'SENT:' MH0/decode-insPen${inspen}/test/LOG)
    echo $resSent >> $fname_res
    resWord=$(grep 'WORD:' MH0/decode-insPen${inspen}/test/LOG)
    echo $resWord >> $fname_res
done
# Plotting results
xaxis="Insertion Penalty"
echo "Plotting Defaul ANN insertion penaly tuning results"
python3 ./monophone_plots.py $fname_res $fname_plot $xaxis
