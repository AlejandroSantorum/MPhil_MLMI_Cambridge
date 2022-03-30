mkdir tmp

NEW_SGNMT=/rds/project/rds-xyBFuSj0hm0/MLMI8.L2022/src/sgnmt.Nov21

python3 $NEW_SGNMT/decode.py \
            --config_file=$GDBNMTBDIR/configs/wmt18.1.ende.wfsa.adapt.1.ini \
            --range=19:19 \
            --output_path=tmp/winomt \
            --src_test=$GDBNMTBDIR/fairseq.pretrained/winomt.en-de.en.bpe \
            --fst_path=fsts/winomt.sgnmt.wmt18ensemble.1.ga/%d.fst

rm -r ./tmp/*
rmdir tmp