This directory holds the data splits for the negation dataset.

The files are:
negation_train.json
negation_dev.json
negation_test.json

The files contain a list of all sentences in each split, with a unique identifier:
XXXXXX-XX-XX, which stands for document_id - paragraph - sentence.

Each sentence has the following keys:
  text, the tokenized original sentence, as one string
  negation, a dictionary of the negation data
  sent_id = the id of the sentence, as described above
  
  Each negation has:
    Cue
    Scope
    Affixal
    
