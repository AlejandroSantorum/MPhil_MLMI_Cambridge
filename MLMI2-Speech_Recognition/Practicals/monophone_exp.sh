
fname_results=./results/monophone_results.txt
maxMixGauss=4

### MONOPHONES USING FILTER BANK
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
            ../tools/steps/step-decode -BEAMWIDTH 200 $PWD/FBK${param}_${mode}/mono hmm${numGauss}4 FBK${param}_${mode}/decode-mono-hmm${numGauss}4
            # Fetching data
            echo "===== FBK${param}_${mode} numberGaussians=${numGauss} =====" >> $fname_results
            resSent=$(grep 'SENT:' FBK${param}_${mode}/decode-mono-hmm${numGauss}4/test/LOG)
            echo $resSent >> $fname_results
            resWord=$(grep 'WORD:' FBK${param}_${mode}/decode-mono-hmm${numGauss}4/test/LOG)
            echo $resWord >> $fname_results
        done
    done
done

### MONOPHONES USING MFCCs
# Lopping through initialisation mode
for mode in Init #FlatStart
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
            ../tools/steps/step-decode -BEAMWIDTH 200 $PWD/MFC${param}_${mode}/mono hmm${numGauss}4 MFC${param}_${mode}/decode-mono-hmm${numGauss}4
            # Fetching data
            echo "===== MFC${param}_${mode} numberGaussians=${numGauss} =====" >> $fname_results
            resSent=$(grep 'SENT:' MFC${param}_${mode}/decode-mono-hmm${numGauss}4/test/LOG)
            echo $resSent >> $fname_results
            resWord=$(grep 'WORD:' MFC${param}_${mode}/decode-mono-hmm${numGauss}4/test/LOG)
            echo $resWord >> $fname_results
        done
    done
done

# Plotting results
python3 ./monophone_plots.py
