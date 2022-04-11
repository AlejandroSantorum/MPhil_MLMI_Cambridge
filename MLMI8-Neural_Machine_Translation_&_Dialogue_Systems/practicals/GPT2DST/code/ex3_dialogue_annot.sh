
dev_or_test=test
N=200000

#source_nlu=$BDIR/hyps/test/nlu_flat_start/model.60000/belief_states.json
source_nlu=hyps/${dev_or_test}/nlu_continued_training/model.${N}/belief_states.json
#dest_dst=hyps/test/cc_dst/nlu_continued_training/model.60000/belief_states.json
dest_dst=hyps/${dev_or_test}/cc_dst/nlu_continued_training/model.${N}/

if ! [ -d "$dest_dst" ]; then
    mkdir $dest_dst
fi

python $BDIR/cc-dst.py --nlu $source_nlu --dst "${dest_dst}belief_states.json"