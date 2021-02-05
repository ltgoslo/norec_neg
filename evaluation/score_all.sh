#! usr/bin/bash

mkdir starsem;

for i in dev test;
do
    python convert_to_starsem.py --in_file ../data/negation_${i}.json --out_file starsem/neg_${i}.starsem --format json;
done

folders=`ls ../data/neg_graphs/*/ -d`
setups=`for i in $folders; do x=${i%*/};echo ${x##*/}; done`

for setup in $setups;
do
    DIR=starsem/$setup;
    mkdir $DIR;
    echo $setup;
    for i in dev test;
    do
        echo $i;
        python convert_to_starsem.py --in_file ../data/neg_graphs/${setup}/${i}.conllu --out_file $DIR/${i}.starsem --format conllu;
        perl eval.cd-sco.pl -g starsem/neg_${i}.starsem -s $DIR/${i}.starsem > $DIR/${i}.max_score.eval;
        for r in 1 2 3 4 5;
        do
            echo $r;
            python convert_to_starsem.py --in_file ../experiments/${setup}/$r/${i}.conllu.pred --out_file $DIR/${i}.starsem.$r.pred --format conllu;
            perl eval.cd-sco.pl -g starsem/neg_${i}.starsem -s $DIR/${i}.starsem.$r.pred > $DIR/${i}.run_${r}.eval;
            grep  -B 7 "Full negation:" $DIR/${i}.run_${r}.eval | cut -d "|" -f1,6-8;
        done
    done
done
