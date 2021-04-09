#!/usr/bin/bash
# Set some random seeds that will be the same for all experiments
SEEDS=(1234 5678 9101112 13141516 17181920)


for SETUP in point_to_root head_first head_first-inside_label head_final head_final-inside_label head_final-inside_label-dep_edges head_final-inside_label-dep_edges-dep_labels; do
    mkdir experiments/$SETUP;
    # Run 5 runs, each with a different random seed to get the variation
    echo "Running $SETUP"
    for RUN in 1 2 3 4 5; do
        i=$(($RUN - 1))
        SEED=${SEEDS[i]}
        OUTDIR=experiments/$SETUP/$RUN;
        mkdir experiments/$SETUP/$RUN;
        if [ -f "$OUTDIR"/test.conllu.pred ]; then
            echo "$SETUP-$RUN already trained"
        else
            ./scripts/run_neggraph.sh $SETUP $RUN $SEED
        fi
    done;
done;
