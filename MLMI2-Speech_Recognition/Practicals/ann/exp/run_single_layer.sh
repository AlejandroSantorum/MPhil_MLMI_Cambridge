
# MFCCs
pracgmmexp_mfc=~/MLMI2/pracgmm/exp/MFC_E_D_A_Z_FlatStart

cd ~/MLMI2/pracann/exp
../tools/steps/step-dnntrain -GPUID 0 -vvv ../convert/mfc13d/env/environment_E_D_A_Z $pracgmmexp_mfc/align-mono-hmm84/align/timit_train.mlf $pracgmmexp_mfc/mono/hmm84/MMF $pracgmmexp_mfc/mono/hmms.mlist MH0-MFC/dnntrain

../tools/steps/step-decode -BEAMWIDTH 200 $PWD/MH0-MFC/dnntrain hmm0 MH0-MFC/decode


# Filter Bank
pracgmmexp_fbk=~/MLMI2/pracgmm/exp/FBK_D_A_Z_FlatStart

cd ~/MLMI2/pracann/exp
../tools/steps/step-dnntrain -GPUID 0 -vvv ../convert/fbk25d/env/environment_D_A_Z $pracgmmexp_fbk/align-mono-hmm84/align/timit_train.mlf $pracgmmexp_fbk/mono/hmm84/MMF $pracgmmexp_fbk/mono/hmms.mlist MH0-FBK/dnntrain

../tools/steps/step-decode -BEAMWIDTH 200 $PWD/MH0-FBK/dnntrain hmm0 MH0-FBK/decode

