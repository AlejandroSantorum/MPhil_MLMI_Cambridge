
TMP_FST_FILE=fsts/tmp_ex3.fst

if [ "$1" == "-ex" ]; then
    AUX_TEMP_FST_FILE=fsts/aux_tmp_ex3.fst

    fstcompose $GDBNMTBDIR/fsts/wmt18.sgnmt.wmt18ensemble.1/1.fst fsts/T.fst | fstcompose - fsts/wtobpe.fst | fstproject --project_type=output > $TMP_FST_FILE
    # Optimization
    fstdeterminize $TMP_FST_FILE $TMP_FST_FILE
    fstminimize $TMP_FST_FILE $TMP_FST_FILE
    # Remapping start symbol
    fstcompose $TMP_FST_FILE $GDBNMTBDIR/fsts/remapstartsym.fst | fstproject --project_type=output > $AUX_TEMP_FST_FILE

    $GDBNMTBDIR/printstrings.py --fst $AUX_TEMP_FST_FILE --syms $GDBNMTBDIR/fairseq.pretrained/wmap.bpe.de --n 5

    rm -f $TEMP_FST_FILE $AUX_TEMP_FST_FILE
    return
fi

# WMT
for i in {1..2998}
do
    baseline_filename=$GDBNMTBDIR/fsts/wmt18.sgnmt.wmt18ensemble.1/${i}.fst
    output_filename=fsts/wmt18.sgnmt.wmt18ensemble.1.ga/${i}.fst

    # Composing baseline with T + composing with wtobpe
    fstcompose $baseline_filename fsts/T.fst | fstcompose - fsts/wtobpe.fst | fstproject --project_type=output > $TMP_FST_FILE

    # Optimization
    fstdeterminize $TMP_FST_FILE $TMP_FST_FILE
    fstminimize $TMP_FST_FILE $TMP_FST_FILE

    # Remapping start symbol
    fstcompose $TMP_FST_FILE $GDBNMTBDIR/fsts/remapstartsym.fst | fstproject --project_type=output > $output_filename

    # Removing temp files
    rm -f $TMP_FST_FILE
done

# WINO
for i in {1..3888}
do
    baseline_filename=$GDBNMTBDIR/fsts/winomt.sgnmt.wmt18ensemble.1/${i}.fst
    output_filename=fsts/winomt.sgnmt.wmt18ensemble.1.ga/${i}.fst

    # Composing baseline with T + composing with wtobpe
    fstcompose $baseline_filename fsts/T.fst | fstcompose - fsts/wtobpe.fst | fstproject --project_type=output > $TMP_FST_FILE

    # Optimization
    fstdeterminize $TMP_FST_FILE $TMP_FST_FILE
    fstminimize $TMP_FST_FILE $TMP_FST_FILE

    # Remapping start symbol
    fstcompose $TMP_FST_FILE $GDBNMTBDIR/fsts/remapstartsym.fst | fstproject --project_type=output > $output_filename

    # Removing temp files
    rm -f $TMP_FST_FILE
done
