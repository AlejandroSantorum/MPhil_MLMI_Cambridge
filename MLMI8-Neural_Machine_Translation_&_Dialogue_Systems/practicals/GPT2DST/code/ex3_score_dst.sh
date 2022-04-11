
dev_or_test=test
N=200000

#turn_level_file=$BDIR/hyps/test/nlu_flat_start/model.60000/belief_states.json
turn_level_file=hyps/${dev_or_test}/nlu_continued_training/model.${N}/belief_states.json
#dialogue_level_file=hyps/test/cc_dst/nlu_continued_training/model.60000/belief_states.json
dialogue_level_file=hyps/${dev_or_test}/cc_dst/nlu_continued_training/model.${N}/belief_states.json


python $BDIR/multiwoz_dst_score.py --field dst_belief_state  \
        --dst_ref $BDIR/data_preparation/data/multiwoz21/refs/${dev_or_test}/${dev_or_test}_v2.1.json  \
        --h $turn_level_file

python $BDIR/multiwoz_dst_score.py --field dst_belief_state  \
        --dst_ref $BDIR/data_preparation/data/multiwoz21/refs/${dev_or_test}/${dev_or_test}_v2.1.json  \
        --h $dialogue_level_file