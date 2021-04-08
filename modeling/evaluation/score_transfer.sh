#!/bin/bash

setup="head_final-inside_label"
for model in norelmo30 norelmo100; do
    DIR=starsem/$model/$setup;
    mkdir $DIR;
    echo $setup;
    for r in 1 2 3 4 5;
    do
        echo $r;
        python3 convert_to_starsem.py --in_file ../experiments/$model/$setup/$r/test.conllu.pred --out_file $DIR/test.starsem."$r".pred --format conllu;
        perl eval.cd-sco.pl -g starsem/neg_test.starsem -s $DIR/test.starsem.$r.pred > $DIR/test.run_"$r".eval;
        grep  -B 7 "Full negation:" $DIR/test.run_"$r".eval | cut -d "|" -f1,6-8;
    done
done

