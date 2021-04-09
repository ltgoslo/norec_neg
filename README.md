# NoReC_neg

This dataset contains 414 documents annotated with negation cue and the related scope. Four documents have been removed compared to NoReC fine and NoReC eval, as these were found to contain formatting errors in the original documents that interferred with the annotations.

## Overview
This dataset is based on the same documents as the extended version of norec_fine. However, this datasets is annotated without comparing it to the previously labeled data. It therefore contains some negations that overlap with evaluative sentences from these, and some that do not. This data comprises roughly 11,000 sentences across more than 400 reviews and 9 different thematic categories (literature, products, restaurants, etc.), taken from  a subset of the [Norwegian Review Corpus](https://github.com/ltgoslo/norec) (NoReC; [Velldal et al. 2018](http://www.lrec-conf.org/proceedings/lrec2018/pdf/851.pdf)). The data comes with a predefined train/dev/test split (inherited from NoReC), and some key statistics are summarized in the table below, including frequency counts and average token lengths.


| Type              | Train  | Dev    | Test     |  Total  |
| :--------         |-------:|-------:|-------:  |-------: |
| Sentences         |  8,543 |   1531  |    1272 |   11346 |
| --- with negation |  1768  |   301   |    263  |   2332  |
| Cues           	|  2025  |  342    |    305  |   2672  |
| --- min length    |  1     |  1      |    1    |   1     |
| --- max length    |  3     |  2      |    2    |   3     |
| --- ave length    |  1.0   |  1.0    |   1.0   |   1.0   |
| --- discontinuous |  19    |  0      |   2     |   21    |
| --- multiple per sent| 228 |  39     |   37    |   304   |
| --- affixal       | 505    |   88    |   69    |   662   |
| Scopes            | 1995   |  339    |   301   |    2635 |
| --- min length    | 1      |  1      |   1     |   1     |
| --- max length    | 44     |  53     |  27     |  53     |
| --- ave length    |  6.9   |   7.1   |  6.5    |  6.9    |
| --- null          |  30    |  3      |  4      |  37     |
| --- discontinuous |  1403  |  236    |  203    | 1842    |
| --- true discontinuous | 423 |  85   |  58     | 566     |


Null scopes are usually sentences such as "Nei." ("No"), which contain only a negation cue. Many of the negation annotations contain discontinuous scopes because of a negation cue breaking up the scope. True discontinuous scopes, on the other hand, are less common, and are often caused by an adverbial which is out of scope but embedded within a negation scope.


## Annotation guidelines

The full annotation guidelines are distributed with this repo and can be found [here](annotation_guidelines/guidelines.md). A summary can also be found in the [paper](https://www.aclweb.org/anthology/2020.lrec-1.618).

## Terms of use
NoReC_neg inherits the license of the underlying [NoReC](https://github.com/ltgoslo/norec) corpus, copied here for convenience:

The data is distributed under a Creative Commons Attribution-NonCommercial licence (CC BY-NC 4.0), access the full license text here: https://creativecommons.org/licenses/by-nc/4.0/

The licence is motivated by the need to block the possibility of third parties redistributing the orignal reviews for commercial purposes. Note that **machine learned models**, extracted **lexicons**, **embeddings**, and similar resources that are created on the basis of NoReC are not considered to contain the original data and so **can be freely used also for commercial purposes** despite the non-commercial condition.


## JSON format

Each sentence has a dictionary with the following keys and values:

* 'sent_id': unique NoReC identifier for document + paragraph + sentence which lines up with the identifiers from the document and sentence-level NoReC data

* 'text': raw text

* 'negations': list of all negations (dictionaries) in the sentence

Additionally, each negation in a sentence is a dictionary with the following keys and values:

* 'Cue': a list of text and character offsets for the negation cues

* 'Scope': a list of text and character offsets for the negation scopes

* 'Affixal': (True, False). Indicating whether the cue is affixal (prefix,suffix) or not.


```
{
	"sent_id": "400620-03-06",
	"text": "Den så jeg ikke komme .",
	"negations": [
		{
			"Cue": [
				[
					"ikke"
				],
				[
					"11:15"
				]
			],
			"Scope": [
				[
					"Den så jeg",
					"komme"
				],
				[
					"0:10",
					"16:21"
				]
			],
			"Affixal": false
		}
	]
},
```

Note that a single sentence may contain several annotated negations. All negations must contain at least one cue, but it is possible for a negation to be without scope. These cases are mostly short comments with references to earlier sentences. Both cues and scopes can be multiword and discontinuous.

## Importing the data

```
>>> import json
>>> data = {}
>>> for name in ["train", "dev", "test"]:
        with open("data/{0}.json".format(name)) as infile:
            data[name] = json.load(infile)
```



## Requirements for negation graph model
1. Python >= 3.6.1
2. Requires PyTorch version 1.2.0. This needs to be installed first and also depends on whether you would like to install the GPU or CPU version, see the following to install [Pytorch 1.2.0 and it's variants of GPU or CPU version.](https://pytorch.org/get-started/previous-versions/#v120)
3. sklearn
4. tabulate
5. h5py
6. tqdm
7. nltk
8. stanza
9. matplotlib



## Training model
The scripts required to train the dependency graph model for predicting negation is found in the 'modeling' directory.

The first thing to do is to download the Norwegian word embeddings from NLPL

```
wget http://vectors.nlpl.eu/repository/20/58.zip
```

You will then need to set the 'EXTERNAL' variable in 'src/run_neggraph.sh' to point to the downloaded vectors. There is no need to unzip the file.

```
EXTERNAL=../58.zip
```

Next, you will need to convert the json data to CONLLU negation graph format. You can use the script in the 'data' directory, which takes a single argument '--setup' (point_to_root, head_final, head_first, head_final-inside_label, head_first-inside_label). We set point_to_root as the default, as this gives the best results:

```
cd data
python3 convert_to_graph.py --setup point_to_root
cd ..
```

Now you can train a model from the 'modeling' directory using the 'run_neggraph.sh' script. It takes three arguments: the graph setup (point_to_root), the run number (0-5), and the random seed number.
```
cd modeling
./scripts/run_neggraph.sh point_to_root 0 1234
```

Alternatively, you can run the script 'run_experiments.sh' to repeat the experiments from the paper.
```
cd modeling
./scripts/run_experiments.sh
```



## Cite

```
@inproceedings{ovrelid-etal-2020-fine,
    title = "Negation in {N}orwegian: an annotated dataset",
    author = "M{\ae}hlum, Petter  and
      Barnes, Jeremy  and
      Kurtz, Robin and
      {\O}vrelid, Lilja  and
      Velldal, Erik",
    booktitle = "Proceedings of the 23rd Nordic Conference on Computational Linguistics",
    year = "2021",
}

```
