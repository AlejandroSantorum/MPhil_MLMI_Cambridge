fstcompose $GDBNMTBDIR/fsts/wmt18.sgnmt.wmt18ensemble.1/1.fst fsts/T.fst | fstcompose - fsts/wtobpe.fst | fstcompose - $GDBNMTBDIR/fsts/remapstartsym.fst | fstproject --project_type=output > fsts/tmp.fst

$GDBNMTBDIR/printstrings.py --fst fsts/tmp.fst --n 2 --syms $GDBNMTBDIR/fairseq.pretrained/wmap.bpe.de