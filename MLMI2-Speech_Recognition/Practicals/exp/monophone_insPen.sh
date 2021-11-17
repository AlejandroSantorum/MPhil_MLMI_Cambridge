
numGaussMixes=8
mode=FlatStart
xaxis="Insertion Penalty"

limInf=-30
jump=5
limSup=30

# parameters for Filter Bank
fname_fbk_res=./results/monophone_FBK_insPen_res.txt
fname_fbk_plot=./imgs/monophone_FBK_insPen_res.png
param=_D_A_Z
# Testing with different Insertion Penalties
for ((inspen = $limInf; inspen <= limSup; inspen += jump));
do
    # Executing decoding (testing)
    ../tools/steps/step-decode -INSWORD $inspen -BEAMWIDTH 300 $PWD/FBK${param}_${mode}/mono hmm${numGaussMixes}4 FBK${param}_${mode}/decode-mono-hmm${numGaussMixes}4-ins${inspen}
    # Fetching data
    echo "===== MFC${param}_${mode} insertionPenalty=${inspen} =====" >> $fname_fbk_res
    resSent=$(grep 'SENT:' FBK${param}_${mode}/decode-mono-hmm${numGaussMixes}4-ins${inspen}/test/LOG)
    echo $resSent >> $fname_fbk_res
    resWord=$(grep 'WORD:' FBK${param}_${mode}/decode-mono-hmm${numGaussMixes}4-ins${inspen}/test/LOG)
    echo $resWord >> $fname_fbk_res
done
# Plotting results
echo "Plotting Filter Bank results"
python3 ./monophone_plots.py $fname_fbk_res $fname_fbk_plot $xaxis


# parameters for MFCCs
fname_mfc_res=./results/monophone_MFC_insPen_res.txt
fname_mfc_plot=./imgs/monophone_MFC_insPen_res.png
param=_E_D_A_Z
# Testing with different Insertion Penalties
for ((inspen = $limInf; inspen <= limSup; inspen += jump));
do
    # Executing decoding (testing)
    ../tools/steps/step-decode -INSWORD $inspen -BEAMWIDTH 300 $PWD/MFC${param}_${mode}/mono hmm${numGaussMixes}4 MFC${param}_${mode}/decode-mono-hmm${numGaussMixes}4-ins${inspen}
    # Fetching data
    echo "===== MFC${param}_${mode} insertionPenalty=${numGauss} =====" >> $fname_mfc_res
    resSent=$(grep 'SENT:' MFC${param}_${mode}/decode-mono-hmm${numGaussMixes}4-ins${inspen}/test/LOG)
    echo $resSent >> $fname_mfc_res
    resWord=$(grep 'WORD:' MFC${param}_${mode}/decode-mono-hmm${numGaussMixes}4-ins${inspen}/test/LOG)
    echo $resWord >> $fname_mfc_res
done
# Plotting results
echo "Plotting MFCCs results"
python3 ./monophone_plots.py $fname_mfc_res $fname_mfc_plot $xaxis