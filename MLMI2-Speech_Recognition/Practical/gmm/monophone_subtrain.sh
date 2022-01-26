xaxis="Number of Gaussians"
maxMixGauss=20
param=_E_D_A_Z

# MONOPHONES USING MFCCs (EDAZ + FlatStart)
fname_mfc_res=./results/mono_subtrain_MFC_res.txt
fname_mfc_plot=./imgs/mono_subtrain_MFC_res.png


for numGauss in $(seq 2 2 $maxMixGauss)
do
    ../tools/steps/step-decode -SUBTRAIN -BEAMWIDTH 300 $PWD/MFC${param}_FlatStart/mono hmm${numGauss}4 MFC${param}_FlatStart/decode-mono-hmm${numGauss}4-subtrain
    # Fetching data
    echo "===== Train numberGaussians=${numGauss} =====" >> $fname_mfc_res
    resSent=$(grep 'SENT:' MFC${param}_FlatStart/decode-mono-hmm${numGauss}4-subtrain/test/LOG)
    echo $resSent >> $fname_mfc_res
    resWord=$(grep 'WORD:' MFC${param}_FlatStart/decode-mono-hmm${numGauss}4-subtrain/test/LOG)
    echo $resWord >> $fname_mfc_res

    # Reading results for test set (MFC_EDAZ_FlatStart), if they exist
    if [ -d ~/MLMI2/pracgmm/exp/MFC${param}_FlatStart/decode-mono-hmm${numGauss}4 ]; then
        echo "===== Test numberGaussians=${numGauss} =====" >> $fname_mfc_res
        resSent=$(grep 'SENT:' MFC${param}_FlatStart/decode-mono-hmm${numGauss}4/test/LOG)
        echo $resSent >> $fname_mfc_res
        resWord=$(grep 'WORD:' MFC${param}_FlatStart/decode-mono-hmm${numGauss}4/test/LOG)
        echo $resWord >> $fname_mfc_res
    fi
done

# Plotting results
echo "Plotting subtrain/test results"
python3 ./monophone_plots.py $fname_mfc_res $fname_mfc_plot $xaxis