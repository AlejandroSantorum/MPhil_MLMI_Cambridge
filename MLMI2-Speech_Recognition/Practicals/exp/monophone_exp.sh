
xaxis="Number of Gaussians"
maxMixGauss=20

### MONOPHONES USING FILTER BANK
fname_fbk_res=./results/monophone_FBK_res.txt
fname_fbk_plot=./imgs/monophone_FBK_res.png
# Lopping through initialisation mode
for mode in Init FlatStart
do
    # Looping through parameterisations
    for param in _Z _D_Z _D_A_Z
    do
        # Executing training command
        ../tools/steps/step-mono -NUMMIXES $maxMixGauss ../convert/fbk25d/env/environment${param} FBK${param}_${mode}/mono
        # Looping through number of Gaussians 
        for numGauss in $(seq 2 2 $maxMixGauss)
        do
            # Executing decoding (testing)
            ../tools/steps/step-decode -BEAMWIDTH 300 $PWD/FBK${param}_${mode}/mono hmm${numGauss}4 FBK${param}_${mode}/decode-mono-hmm${numGauss}4
            # Fetching data
            echo "===== FBK${param}_${mode} numberGaussians=${numGauss} =====" >> $fname_fbk_res
            resSent=$(grep 'SENT:' FBK${param}_${mode}/decode-mono-hmm${numGauss}4/test/LOG)
            echo $resSent >> $fname_fbk_res
            resWord=$(grep 'WORD:' FBK${param}_${mode}/decode-mono-hmm${numGauss}4/test/LOG)
            echo $resWord >> $fname_fbk_res
        done
    done
done
# Plotting results
echo "Plotting Filter Bank results"
python3 ./monophone_plots.py $fname_fbk_res $fname_fbk_plot $xaxis

### MONOPHONES USING MFCCs
fname_mfc_res=./results/monophone_MFC_res.txt
fname_mfc_plot=./imgs/monophone_MFC_res.png
# Lopping through initialisation mode
for mode in Init FlatStart
do  
    # Looping through parameterisations
    for param in _E_Z _E_D_Z _E_D_A_Z
    do
        # Executing training command
        ../tools/steps/step-mono -NUMMIXES $maxMixGauss ../convert/mfc13d/env/environment${param} MFC${param}_${mode}/mono
        # Looping through number of Gaussians 
        for numGauss in $(seq 2 2 $maxMixGauss)
        do
            # Executing decoding (testing)
            ../tools/steps/step-decode -BEAMWIDTH 300 $PWD/MFC${param}_${mode}/mono hmm${numGauss}4 MFC${param}_${mode}/decode-mono-hmm${numGauss}4
            # Fetching data
            echo "===== MFC${param}_${mode} numberGaussians=${numGauss} =====" >> $fname_mfc_res
            resSent=$(grep 'SENT:' MFC${param}_${mode}/decode-mono-hmm${numGauss}4/test/LOG)
            echo $resSent >> $fname_mfc_res
            resWord=$(grep 'WORD:' MFC${param}_${mode}/decode-mono-hmm${numGauss}4/test/LOG)
            echo $resWord >> $fname_mfc_res
        done
    done
done
# Plotting results
echo "Plotting MFCCs results"
python3 ./monophone_plots.py $fname_mfc_res $fname_mfc_plot $xaxis
