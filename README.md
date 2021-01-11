# NoReC_neg

This dataset contains 414 documents annotated with negation cue and the related scope. Four documents have been removed compared to NoReC fine and NoReC eval, as these were found to contain formatting errors in the original documents that interferred with the annotations. 

## Overview
This dataset is based on the same documents as the extended version of norec_fine. However, this datasets is annotated without comparing it to the previously labeled data. It therefore contains some negations that overlap with evaluative sentences from these, and some that do not. This data comprises roughly 11,000 sentences across more than 400 reviews and 9 different thematic categories (literature, products, restaurants, etc.), taken from  a subset of the [Norwegian Review Corpus](https://github.com/ltgoslo/norec) (NoReC; [Velldal et al. 2018](http://www.lrec-conf.org/proceedings/lrec2018/pdf/851.pdf)). The data comes with a predefined train/dev/test split (inherited from NoReC), and some key statistics are summarized in the table below, including frequency counts and average token lengths.     


| Type              | Train  | Dev    | Test     |  Total  |
| :--------         |-------:|-------:|-------:  |-------: |
| Sentences         |   8634 |   1531  |    1272 |   11437 |
| --- subjective    |  4555  |   821   |    674  |   6050  |
| --- multiple polarities | 660 | 120  |    91   |   871   |
| --- avg. len      | 16.7   | 16.9    |    17.2 |   16.8  |
| Holders           |   898  |     120 |     110 |    1128 |
| --- unique        |  585   |  88     | 73      |   746   |
| --- avg. len      |   1.1  |     1.0 |     1.0 |    1.1  |
| --- avg. per subj sent |  0.1  |  0.1  |  0.1  |    0.1  |
| Targets           |   6778 |    1152 |    993  |   8923  |
| --- unique        | 5000   |    871  |    729  |   6699  |
| --- avg. len      |   1.9  |    2.0  |    2.0  |   2.0   |
| --- avg. per subj sent |  1.1  |  1.1  |  1.1  |   1.1   |
| --- discontinuous |39      |     5   |    6    |   50    |
| --- Not On Topic  |  971   |     226 |   148   |  1345   |
| Polar Expressions |  8448  |   1432  |    1235 |   11115 |
| --- unique        | 8071   |   1390  |    1190 |   10651 |
| --- avg. len      |   4.9  |     5.1 |     4.9 |  4.9    |
| --- avg. per subj sent |  1.8  |  1.7  |  1.8  |  1.8    |
| --- discontiuous  |  783   |     131 |    125  |   1039  |


Each opinion is annotated for _polarity_ (positive, negative) and _intensity_ (slight, standard, strong). The distribution is shown in the figure below:

![Polarity Distribution](annotation_guidelines/images/distribution.png)


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

## Cite

