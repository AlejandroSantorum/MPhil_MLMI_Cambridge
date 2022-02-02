#!/bin/bash

if [ $# != 2 ]
then
    echo "Usage: `basename $0` xml scoring-dir"
    echo "e,g, : `basename $0` word.xml scoring"
    exit 1
fi

export PATH=/usr/local/teach/scoring/F4DE-3.2.4/bin:/usr/local/teach/perl/perls/perl-5.16.3/bin:$PATH

SRCXML=$1
TGTDIR=$2

name=`basename $SRCXML .xml`

if [ -d "$TGTDIR/${name}" ]
then
    echo "Delete scoring directory $TGTDIR/${name} to rerun"
    exit 1
fi


# create directories for scoring

mkdir -p $TGTDIR/${name}-tmp
mkdir -p $TGTDIR/${name}

cp $SRCXML $TGTDIR/${name}.kwslist.xml

BABEL13_Scorer -sys $TGTDIR/${name}.kwslist.xml -dbDir /usr/local/teach/MLSALT5/Practical/IndusDB -comp $TGTDIR/${name}-tmp -res $TGTDIR/${name} -exp KWS13_CUED_IARPA-babel202b-v1.0d_conv-dev_BaDev_KWS_FullLP_BaseLR_NTAR_p-test_1 >& $TGTDIR/${name}.LOG

# tidy-up scoring and copy generated files

rm -r $TGTDIR/${name}-tmp

if [ -e "$TGTDIR/${name}/Ensemble.AllOccur.results.txt" ]
then
    cp $TGTDIR/${name}/Ensemble.AllOccur.png $TGTDIR/${name}-det.png
    cp $TGTDIR/${name}/Ensemble.AllOccur.results.txt  $TGTDIR/${name}-res.txt
else 
    echo "Scoring failed - check format of xml file: $SRCXML"
fi



