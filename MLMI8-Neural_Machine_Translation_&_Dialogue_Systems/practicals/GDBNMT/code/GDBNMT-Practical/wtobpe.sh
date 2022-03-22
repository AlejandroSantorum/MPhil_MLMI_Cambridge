INPUT_MAPPING_FILE=$GDBNMTBDIR/fsts/w+l.map.de
OUTPUT_MAPPING_FILE=$GDBNMTBDIR/fairseq.pretrained/wmap.bpe.de

# get txt representation of FST
python3 ./pyscripts/wtobpe.py
# compile FST
fstcompile --isymbols=$INPUT_MAPPING_FILE --osymbols=$OUTPUT_MAPPING_FILE --keep_isymbols --keep_osymbols  fsts/wtobpe.txt fsts/wtobpe.fst
# Sorting by input space
fstarcsort --sort_type=ilabel fsts/wtobpe.fst fsts/wtobpe.fst

if [ "$1" == "-ex" ]; then
    TEMP_FST_FILE=fsts/tmp_ex2_1.fst

    # Applying wtobpe.fst and T.fst, followed by output projection...
    fstcompose $GDBNMTBDIR/fsts/wmt18.sgnmt.wmt18ensemble.1/1.fst fsts/T.fst | fstcompose - fsts/wtobpe.fst | fstproject --project_type=output > $TEMP_FST_FILE
    # ... yield a WFSA with gendered alternatives in their subword form:
    $GDBNMTBDIR/printstrings.py --fst $TEMP_FST_FILE --n 5 --syms $GDBNMTBDIR/fairseq.pretrained/wmap.bpe.de

    rm -f $TEMP_FST_FILE
fi