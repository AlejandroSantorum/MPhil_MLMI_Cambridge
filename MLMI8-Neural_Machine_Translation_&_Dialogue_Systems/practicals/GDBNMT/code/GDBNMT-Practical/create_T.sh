# inverting wtoc to get mapping classes to words
fstinvert fsts/wtoc.fst fsts/ctow.fst

# sorting labels of both FSTs so they can be composed
fstarcsort --sort_type=ilabel fsts/wtoc.fst fsts/wtoc.fst
fstarcsort --sort_type=ilabel fsts/ctow.fst fsts/ctow.fst

# composing them
fstcompose fsts/wtoc.fst fsts/ctow.fst fsts/T.fst

if [ "$1" == "-ex" ]; then
    TEMP_FST_FILE=fsts/tmp_ex1_2.fst
    MAPPING_FILE=$GDBNMTBDIR/fsts/w+l.map.de

    fstcompose $GDBNMTBDIR/fsts/wmt18.sgnmt.wmt18ensemble.1/1.fst fsts/T.fst > $TEMP_FST_FILE

    echo "Input baseline translation:"
    $GDBNMTBDIR/printstrings.py --fst $TEMP_FST_FILE --n 2 --syms $MAPPING_FILE

    echo "Some sentences that contains alternative gendered versions of the input baseline translation:"
    $GDBNMTBDIR/printstrings.py --fst $TEMP_FST_FILE --n 5 --syms $MAPPING_FILE --project_output

    rm -f $TEMP_FST_FILE
fi