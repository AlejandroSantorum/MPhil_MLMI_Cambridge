
echo "Development set DST Joint Accuracy:"
python $BDIR/multiwoz_dst_score.py --field dst_belief_state \
        --dst_ref $BDIR/data_preparation/data/multiwoz21/refs/dev/dev_v2.1.json \
        --h ./hyps/ex4/dev/nlu_continued_training/model.200000/belief_states.json

echo ""
echo "Test set DST Joint Accuracy:"
python $BDIR/multiwoz_dst_score.py --field dst_belief_state \
        --dst_ref $BDIR/data_preparation/data/multiwoz21/refs/test/test_v2.1.json \
        --h ./hyps/ex4/test/nlu_continued_training/model.200000/belief_states.json
