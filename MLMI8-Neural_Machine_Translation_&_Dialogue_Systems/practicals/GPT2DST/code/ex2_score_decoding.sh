
decoding_file=./hyps/test/nlu_continued_training/model.200000/belief_states.json

python $BDIR/multiwoz_dst_score.py --field nlu_belief_state \
        --dst_ref $BDIR/data_preparation/data/multiwoz21/refs/test/test_v2.1.json \
        --h $decoding_file