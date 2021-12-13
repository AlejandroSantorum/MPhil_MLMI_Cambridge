
fixed_TB=1000
fixed_numMixes=12
inspen=-10
param=MFC_E_D_A_Z_FlatStart/
fname_res=./results/triphone_varyRO_res.txt
fname_plot=./imgs/triphone_varyRO_res.png

if [ "$1" == "-d" ]; then
    rm -rf `find ./${param} -name '*xwtri-varyRO*'`
    rm -rf $fname_res
fi

##########################################
# RO TUNING

# RO value
infRO=100
supRO=500
jumpRO=50
##########################################

# Testing with different Insertion Penalties
for ((valRO = infRO; valRO <= supRO; valRO += jumpRO));
do
    # Executing training
    ../tools/steps/step-xwtri -NUMMIXES $fixed_numMixes -ROVAL $valRO -TBVAL $fixed_TB $PWD/${param}mono hmm14 ${param}xwtri-varyRO${valRO}-TB${fixed_TB}

    # Executing decoding (testing)
    ../tools/steps/step-decode -INSWORD $inspen -BEAMWIDTH 300 $PWD/${param}xwtri-varyRO${valRO}-TB${fixed_TB} hmm${fixed_numMixes}4 ${param}decode-xwtri-varyRO${valRO}-TB${fixed_TB}-NM${fixed_numMixes}
    # Fetching data
    echo "===== xwtri RO=${valRO} TB=${fixed_TB} numMix=${fixed_numMixes} =====" >> $fname_res
    resClustStates=$(grep 'CO: HMM' ${param}xwtri-varyRO${valRO}-TB${fixed_TB}/hmm10/LOG)
    echo $resClustStates >> $fname_res
    resSent=$(grep 'SENT:' ${param}decode-xwtri-varyRO${valRO}-TB${fixed_TB}-NM${fixed_numMixes}/test/LOG)
    echo $resSent >> $fname_res
    resWord=$(grep 'WORD:' ${param}decode-xwtri-varyRO${valRO}-TB${fixed_TB}-NM${fixed_numMixes}/test/LOG)
    echo $resWord >> $fname_res
done
# Plotting results
echo "Plotting results"
xaxis="RO value"
python3 ./monophone_plots.py $fname_res $fname_plot $xaxis