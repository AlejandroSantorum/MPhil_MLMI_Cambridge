
xaxis="Number of Gaussians"
maxMixGauss=20

######################################################
### MONOPHONES USING FILTER BANK
fname_fbk_res=./results/monophone_FBK_res.txt
fname_fbk_plot=./imgs/monophone_FBK_res.png

### INIT ###
# Looping through parameterisations
for param in _Z _D_Z _D_A_Z
do
    # Executing training command
    ../tools/steps/step-mono -NUMMIXES $maxMixGauss ../convert/fbk25d/env/environment${param} FBK${param}_Init/mono
    # Looping through number of Gaussians 
    for numGauss in $(seq 2 2 $maxMixGauss)
    do
        # Executing decoding (testing)
        ../tools/steps/step-decode -BEAMWIDTH 300 $PWD/FBK${param}_Init/mono hmm${numGauss}4 FBK${param}_Init/decode-mono-hmm${numGauss}4
        # Fetching data
        echo "===== FBK${param}_Init numberGaussians=${numGauss} =====" >> $fname_fbk_res
        resSent=$(grep 'SENT:' FBK${param}_Init/decode-mono-hmm${numGauss}4/test/LOG)
        echo $resSent >> $fname_fbk_res
        resWord=$(grep 'WORD:' FBK${param}_Init/decode-mono-hmm${numGauss}4/test/LOG)
        echo $resWord >> $fname_fbk_res
    done
done
### FLATSTART ###
# Looping through parameterisations
for param in _Z _D_Z _D_A_Z
do
    # Executing training command
    ../tools/steps/step-mono -FLATSTART -NUMMIXES $maxMixGauss ../convert/fbk25d/env/environment${param} FBK${param}_FlatStart/mono
    # Looping through number of Gaussians 
    for numGauss in $(seq 2 2 $maxMixGauss)
    do
        # Executing decoding (testing)
        ../tools/steps/step-decode -BEAMWIDTH 300 $PWD/FBK${param}_FlatStart/mono hmm${numGauss}4 FBK${param}_FlatStart/decode-mono-hmm${numGauss}4
        # Fetching data
        echo "===== FBK${param}_FlatStart numberGaussians=${numGauss} =====" >> $fname_fbk_res
        resSent=$(grep 'SENT:' FBK${param}_FlatStart/decode-mono-hmm${numGauss}4/test/LOG)
        echo $resSent >> $fname_fbk_res
        resWord=$(grep 'WORD:' FBK${param}_FlatStart/decode-mono-hmm${numGauss}4/test/LOG)
        echo $resWord >> $fname_fbk_res
    done
done
# Plotting results
echo "Plotting Filter Bank results"
python3 ./monophone_plots.py $fname_fbk_res $fname_fbk_plot $xaxis


######################################################
### MONOPHONES USING MFCCs
fname_mfc_res=./results/monophone_MFC_res.txt
fname_mfc_plot=./imgs/monophone_MFC_res.png

### INIT ###
# Looping through parameterisations
for param in _E_Z _E_D_Z _E_D_A_Z
do
    # Executing training command
    ../tools/steps/step-mono -NUMMIXES $maxMixGauss ../convert/mfc13d/env/environment${param} MFC${param}_Init/mono
    # Looping through number of Gaussians 
    for numGauss in $(seq 2 2 $maxMixGauss)
    do
        # Executing decoding (testing)
        ../tools/steps/step-decode -BEAMWIDTH 300 $PWD/MFC${param}_Init/mono hmm${numGauss}4 MFC${param}_Init/decode-mono-hmm${numGauss}4
        # Fetching data
        echo "===== MFC${param}_Init numberGaussians=${numGauss} =====" >> $fname_mfc_res
        resSent=$(grep 'SENT:' MFC${param}_Init/decode-mono-hmm${numGauss}4/test/LOG)
        echo $resSent >> $fname_mfc_res
        resWord=$(grep 'WORD:' MFC${param}_Init/decode-mono-hmm${numGauss}4/test/LOG)
        echo $resWord >> $fname_mfc_res
    done
done
### FLATSTART ###
# Looping through parameterisations
for param in _E_Z _E_D_Z _E_D_A_Z
do
    # Executing training command
    ../tools/steps/step-mono -FLATSTART -NUMMIXES $maxMixGauss ../convert/mfc13d/env/environment${param} MFC${param}_FlatStart/mono
    # Looping through number of Gaussians 
    for numGauss in $(seq 2 2 $maxMixGauss)
    do
        # Executing decoding (testing)
        ../tools/steps/step-decode -BEAMWIDTH 300 $PWD/MFC${param}_FlatStart/mono hmm${numGauss}4 MFC${param}_FlatStart/decode-mono-hmm${numGauss}4
        # Fetching data
        echo "===== MFC${param}_FlatStart numberGaussians=${numGauss} =====" >> $fname_mfc_res
        resSent=$(grep 'SENT:' MFC${param}_FlatStart/decode-mono-hmm${numGauss}4/test/LOG)
        echo $resSent >> $fname_mfc_res
        resWord=$(grep 'WORD:' MFC${param}_FlatStart/decode-mono-hmm${numGauss}4/test/LOG)
        echo $resWord >> $fname_mfc_res
    done
done
# Plotting results
echo "Plotting MFCCs results"
python3 ./monophone_plots.py $fname_mfc_res $fname_mfc_plot $xaxis
