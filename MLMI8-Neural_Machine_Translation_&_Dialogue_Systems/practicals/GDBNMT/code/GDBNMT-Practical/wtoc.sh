
MAPPING_FILE=$GDBNMTBDIR/fsts/w+l.map.de

# get txt representation of FST
python3 ./pyscripts/wtoc.py
# compile FST
fstcompile --isymbols=$MAPPING_FILE --osymbols=$MAPPING_FILE --keep_isymbols --keep_osymbols  fsts/wtoc.txt fsts/wtoc.fst
# compose FST with acceptors
fstcompose $GDBNMTBDIR/fsts/wmt18.sgnmt.wmt18ensemble.1/1.fst fsts/wtoc.fst tmp.fst