
MAPPING_FILE=$GDBNMTBDIR/fsts/w+l.map.de

# get txt representation of FST
python3 ./pyscripts/wtoc.py
# compile FST
fstcompile --isymbols=$MAPPING_FILE --osymbols=$MAPPING_FILE --keep_isymbols --keep_osymbols  fsts/wtoc.txt fsts/wtoc.fst

if [ "$1" == "-ex" ]; then
    TEMP_FST_FILE=fsts/tmp_ex1_1.fst

    # compose FST with acceptors
    fstcompose $GDBNMTBDIR/fsts/wmt18.sgnmt.wmt18ensemble.1/1.fst fsts/wtoc.fst $TEMP_FST_FILE

    echo "Input baseline translation:"
    $GDBNMTBDIR/printstrings.py --fst $TEMP_FST_FILE --syms $MAPPING_FILE --n 2

    echo "Some sentences that contains possible class mappings:"
    $GDBNMTBDIR/printstrings.py --fst $TEMP_FST_FILE --syms $MAPPING_FILE --n 2 --project_output

    rm -f $TEMP_FST_FILE
fi