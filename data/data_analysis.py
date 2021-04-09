import os
from nltk import FreqDist
from nltk.corpus import stopwords
import re
import numpy as np
import matplotlib.pyplot as plt
import argparse
import json



def multiple(sent, label="Cues"):
    negs = sent["negations"]
    if len(negs) > 1:
        #print("-"*40)
        #print("MULTIPLE")
        #print(sent)
        #print("-"*40)
        return 1
    else:
        return 0

def true_discontinuous(negation):
    # get all of the beginning and end character idxs for the cue and scope
    scopes = []
    for offset in negation["Cue"][1]:
        bidx, eidx = offset.split(":")
        scopes.append((int(bidx), int(eidx)))
    for offset in negation["Scope"][1]:
        bidx, eidx = offset.split(":")
        scopes.append((int(bidx), int(eidx)))
    # sort them
    scopes = sorted(scopes)
    # if there's a distance of more than 1 between them, it is truly discontinuous
    for i, (bidx, eidx) in enumerate(scopes):
        if i < len(scopes) - 1:
            next_bidx = scopes[i+1][0]
            if abs(eidx - next_bidx) > 1:
                #print(scopes)
                #print("Truly discontinuous")
                return 1
    return 0

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--normalize", action="store_true")
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--data_dir", default=".")

    args = parser.parse_args()

    num_sents = {"train": 0, "dev": 0, "test": 0}
    num_neg_sents = {"train": 0, "dev": 0, "test": 0}
    sent_lengths = {"train": [], "dev": [], "test": []}

    num_scopes = {"train": 0, "dev": 0, "test": 0}
    scopes_lengths = {"train": [], "dev": [], "test": []}

    num_cues = {"train": 0, "dev": 0, "test": 0}
    cues_lengths = {"train": [], "dev": [], "test": []}

    discontinuous_cues = {"train": 0, "dev": 0, "test": 0}
    discontinuous_scopes = {"train": 0, "dev": 0, "test": 0}
    true_discontinuous_scopes = {"train": 0, "dev": 0, "test": 0}
    null_scopes = {"train": 0, "dev": 0, "test": 0}

    affixals = {"train": 0, "dev": 0, "test": 0}

    mult_cues = {"train": 0, "dev": 0, "test": 0}
    mult_scopes = {"train": 0, "dev": 0, "test": 0}


    for split in ["train", "dev", "test"]:
        with open(os.path.join(args.data_dir, "negation_" + split + ".json")) as infile:
            data = json.load(infile)
        for sentence in data:
            # get SENTENCE DATA
            num_sents[split] += 1
            sent_lengths[split].append(len(sentence["text"].split()))
            mult_cues[split] += multiple(sentence, "Cue")
            #mult_target[split] += multiple(sentence, "Scope")
            if len(sentence["negations"]) > 0:
                num_neg_sents[split] += 1
            for negation in sentence["negations"]:
                #NOT = opinion["NOT"]
                #if NOT is True:
                #    not_on_topic[split] += 1
                cue = negation["Cue"][0]
                # continue only if there actually is a cue
                if cue != []:
                    num_cues[split] += 1
                    if len(cue) > 1:
                        discontinuous_cues[split] += 1
                        #print("-"*40)
                        #print("DISCONTINUOUS")
                        #print(sentence)
                        #print("-"*40)
                    cue_len = 0
                    for text in cue:
                        cue_len += len(text.split())
                    cues_lengths[split].append(cue_len)
                # continue only if there actually is a scope
                scope = negation["Scope"][0]
                if scope != []:
                    num_scopes[split] += 1
                    if len(scope) > 1:
                        discontinuous_scopes[split] += 1
                        true_discontinuous_scopes[split] += true_discontinuous(negation)
                        #print("-"*40)
                        #print("DISCONTINUOUS")
                        #print(sentence)
                        #print("-"*40)
                    scope_len = 0
                    for text in scope:
                        scope_len += len(text.split())
                    scopes_lengths[split].append(scope_len)
                else:
                    null_scopes[split] += 1
                if negation["Affixal"]:
                    affixals[split] += 1

    for split in ["train", "dev", "test"]:
        print("{} ############################################".format(split))
        print("Sents: {0}".format(num_sents[split]))
        print("---- negated: {0}".format(num_neg_sents[split]))
        #print("---- min len: {0}".format(np.min(sent_lengths[split])))
        #print("---- max len: {0}".format(np.max(sent_lengths[split])))
        #print("---- ave len: {0:.1f}".format(np.mean(sent_lengths[split])))
        print()
        print("Cues: {0}".format(num_cues[split]))
        print("---- min len: {0}".format(np.min(cues_lengths[split])))
        print("---- max len: {0}".format(np.max(cues_lengths[split])))
        print("---- ave len: {0:.1f}".format(np.mean(cues_lengths[split])))
        print("---- discontinuous: {0}".format(discontinuous_cues[split]))
        print("---- Mult. per sent {0}".format(mult_cues[split]))
        print("---- Affixal.: {0}".format(affixals[split]))
        print()
        print("Scopes: {0}".format(num_scopes[split]))
        print("---- min len: {0}".format(np.min(scopes_lengths[split])))
        print("---- max len: {0}".format(np.max(scopes_lengths[split])))
        print("---- ave len: {0:.1f}".format(np.mean(scopes_lengths[split])))
        print("---- null: {0}".format(null_scopes[split]))
        print("---- discontinuous: {0}".format(discontinuous_scopes[split]))
        print("---- true discontinuous: {0}".format(true_discontinuous_scopes[split]))
        print()




    print("Total###########################")
    total = np.sum(list(num_sents.values()))
    print("Sents: {0}".format(total))
    print("---- negated: {0}".format(np.sum(list(num_neg_sents.values()))))
    all_sent_lengths = [i for k in sent_lengths.values() for i in k]
    #print("---- min len: {0}".format(np.min(all_sent_lengths)))
    #print("---- max len: {0}".format(np.max(all_sent_lengths)))
    #print("---- ave len: {0:.1f}".format(np.mean(all_sent_lengths)))
    print()

    # HOLDERS
    total_holders = np.sum(list(num_cues.values()))
    print("Cues: {0}".format(total_holders))
    all_source_lengths = [i for k in cues_lengths.values() for i in k]
    print("---- min len: {0}".format(np.min(all_source_lengths)))
    print("---- max len: {0}".format(np.max(all_source_lengths)))
    print("---- ave len: {0:.1f}".format(np.mean(all_source_lengths)))
    print("---- discontinuous: {0}".format(np.sum(list(discontinuous_cues.values())) ))
    print("---- Mult. per sent: {0}".format(np.sum(list(mult_cues.values()))))
    print("---- Affixals: {}".format(np.sum(list(affixals.values()))))
    print()

    # TARGETS
    total_targets = np.sum(list(num_scopes.values()))
    print("Targets: {0}".format(total_targets))
    all_targ_lengths = [i for k in scopes_lengths.values() for i in k]
    print("---- min len: {0}".format(np.min(all_targ_lengths)))
    print("---- max len: {0}".format(np.max(all_targ_lengths)))
    print("---- ave len: {0:.1f}".format(np.mean(all_targ_lengths)))
    print("---- discontinuous: {0}".format(np.sum(list(discontinuous_scopes.values()))))
    print("---- true discontinuous: {0}".format(np.sum(list(true_discontinuous_scopes.values()))))
    print()

