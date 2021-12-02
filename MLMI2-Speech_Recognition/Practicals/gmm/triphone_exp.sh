
inspen=8
param=MFC_E_D_A_Z_FlatStart/
fname_res=./results/triphone_res.txt

if [ "$1" == "-d" ]; then
    rm -rf `find ./${param} -name '*xwtri*'`
    rm -rf $fname_res
fi

##########################################
# GRID-SEARCH HYPERPARAMETER TUNING

# Number of Gaussian Mixture Components
infNumMix=4
supNumMix=12
jumpNumMix=4

# RO value
infRO=100
supRO=300
jumpRO=100

# TB value
infTB=600
supTB=1000
jumpTB=200
##########################################

# Testing with different Insertion Penalties
for ((valRO = infRO; valRO <= supRO; valRO += jumpRO));
do
    for ((valTB = infTB; valTB <= supTB; valTB += jumpTB));
    do
        # Executing training
        ../tools/steps/step-xwtri -NUMMIXES $supNumMix -ROVAL $valRO -TBVAL $valTB $PWD/${param}mono hmm14 ${param}xwtri-RO${valRO}-TB${valTB}

        for ((numMix = infNumMix; numMix <= supNumMix; numMix += jumpNumMix));
        do
        # Executing decoding (testing)
        ../tools/steps/step-decode -CORETEST -BEAMWIDTH 300 $PWD/${param}xwtri-RO${valRO}-TB${valTB} hmm${numMix}4 ${param}decode-xwtri-RO${valRO}-TB${valTB}-NM${numMix}
        # Fetching data
        echo "===== xwtri RO=${valRO} TB=${valTB} numMix=${numMix} =====" >> $fname_res
        resClustStates=$(grep 'CO: HMM' ${param}xwtri-RO${valRO}-TB${valTB}/hmm10/LOG)
        echo $resClustStates >> $fname_res
        resSent=$(grep 'SENT:' ${param}decode-xwtri-RO${valRO}-TB${valTB}-NM${numMix}/test/LOG)
        echo $resSent >> $fname_res
        resWord=$(grep 'WORD:' ${param}decode-xwtri-RO${valRO}-TB${valTB}-NM${numMix}/test/LOG)
        echo $resWord >> $fname_res
        done
    done
done
