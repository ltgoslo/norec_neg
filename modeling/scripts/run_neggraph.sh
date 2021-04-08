#!/bin/bash
#
#SBATCH --job-name=sentgraph --account=nn9851k
#SBATCH --output=sentgraph.out
#SBATCH --partition=normal
#SBATCH -n 1
#SBATCH -t 10:00:00
#SBATCH --mem 8GB
#XSBATCH --mail-type=ALL
#SBATCH --mail-user=jeremycb@ifi.uio.no
#

module purge


module use -a /cluster/shared/nlpl/software/modules/etc
module load nlpl-pytorch/1.5.0/3.7
module load nlpl-gensim/3.8.2/3.7

SETUP=$1;
RUN=$2;
SEED=$3;


# EXTERNAL EMBEDDINGS
############################
echo "###########################"
echo EXTERNAL EMBEDDINGS
echo "###########################"


EXTERNAL=/cluster/shared/nlpl/data/vectors/20/58.zip
echo using external vectors: $EXTERNAL
echo

# INPUT FILES
############################
echo "###########################"
echo INPUT FILES
echo "###########################"

TRAIN=../data/neg_graphs/$SETUP/train.conllu
DEV=../data/neg_graphs/$SETUP/dev.conllu
TEST=../data/neg_graphs/$SETUP/test.conllu

echo train data: $TRAIN
echo dev data: $DEV
echo test data: $TEST
echo

# OUTPUT DIR
############################
echo "###########################"
echo OUTPUT DIR
echo "###########################"

DIR=experiments/$SETUP/$RUN
echo saving experiment to $DIR

rm -rf $DIR
mkdir $DIR

python ./src/main.py --config configs/base.cfg --train $TRAIN --val $DEV --predict_file $TEST --dir $DIR --external $EXTERNAL --seed $SEED
    #--seed $SEED

rm $DIR/best_model.save
rm $DIR/last_epoch.save
