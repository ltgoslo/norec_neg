import norec
import argparse
import os
import json
import stanza

from nltk.tokenize.simple import SpaceTokenizer

tk = SpaceTokenizer()

nlp = stanza.Pipeline("no",
                      processors="tokenize,lemma,pos,depparse",
                      tokenize_pretokenized=True)

def tag_json_files(json_file):
    for i, sentence in enumerate(json_file):
        try:
            tagged_sent = nlp(sentence["text"])
            conllu = ""
            for token in tagged_sent.iter_tokens():
                tok = token.words[0]
                conllu += "{}\t{}\t{}\t{}\t_\t_\t{}\t{}\t_\t_\n".format(tok.id, tok.text, tok.lemma, tok.upos, tok.head, tok.deprel)
            sentence["conllu"] = conllu
        except:
            #print(i)
            print(sentence["sent_id"])

def get_bio(negation, label="Cue"):
    try:
        text, idxs = negation[label]
    # will throw exception if the opinion target is None type
    except TypeError:
        return []
    except ValueError:
        return []
    # get the beginning and ending indices
    if len(text) > 1:
        updates = []
        #
        for t, idx in zip(text, idxs):
            bidx, eidx = idx.split(":")
            bidx = int(bidx)
            eidx = int(eidx)
            target_tokens = t.split()
            #
            tags = []
            for i, token in enumerate(target_tokens):
                tags.append(label.lower())
            updates.append((bidx, tags))
        return updates
    else:
        bidx, eidx = idxs[0].split(":")
        bidx = int(bidx)
        eidx = int(eidx)
        target_tokens = text[0].split()
        #
        tags = []
        for i, token in enumerate(target_tokens):
            tags.append(label.lower())
        return [(bidx, tags)]

def replace_with_labels(labels, offsets, bidx, tags):
    # normal cues and scopes
    if bidx in offsets:
        token_idx = offsets.index(bidx)
        for i, tag in enumerate(tags):
            labels[i + token_idx] = tag
    # affixal cues
    else:
        # if the affixal cue is in the last word in the sentence, set the token_idx to that index
        if bidx > offsets[-1]:
            token_idx = len(offsets) - 1
        # Otherwise set token_idx to be the idx of the word the affixal cue appears in
        else:
            for i, x in enumerate(offsets):
                if x > bidx:
                    token_idx = i - 1
                    break
        for i, tag in enumerate(tags):
            labels[i + token_idx] = tag
    return labels


def create_labels(text, negation):
    """
    Converts a text (each token separated by a space) and a negation expression
    into a list of labels for each token in the text.
    """
    offsets = [l[0] for l in tk.span_tokenize(text)]
    #
    labels = ["O"] * len(offsets)
    #
    anns = []
    try:
        anns.extend(get_bio(negation, "Scope"))
    except:
        pass
    try:
        anns.extend(get_bio(negation, "Cue"))
    except:
        pass
    #
    for bidx, tags in anns:
        labels = replace_with_labels(labels, offsets, bidx, tags)
    return labels

def create_negation_dict(labels, setup="point_to_root", inside_label=False):
    """
    point_to_root: the final token of the sentiment expression is set as the root and all other labels point to this

    head_first: the first token in the sentiment expression is the root, and the for the holder and target expressions, the first token connects to the root, while the other tokens connect to the first

    head final: the final token in the sentiment expression is the root, and the for the holder and target expressions, the final token connects to the root, while the other tokens connect to the final
    """
    sent_dict = {}
    #
    # associate each label with its token_id
    enum_labels = [(i + 1, l) for i, l in enumerate(labels)]
    #
    if setup in ["point_to_root", "head_final"]:
        enum_labels = list(reversed(enum_labels))
    #
    #for token_id, label in reversed(enum_labels):
    for token_id, label in enum_labels:
        if "cue" in label:
            sent_dict[token_id] = "0:{0}".format(label)
            cue_root_id = token_id
            break
    #
    # point_to_root: point to exp_root_id, regardless of expression type
    if setup == "point_to_root":
        for token_id, label in enum_labels:
            if label == "O":
                sent_dict[token_id] = "_"
            else:
                if token_id not in sent_dict.keys():
                    sent_dict[token_id] = "{0}:{1}".format(cue_root_id, label)
    # head_first or head_final: first/final point to exp_root, others point inside expression
    else:
        for token_id, label in enum_labels:
            if "scope" in label:
                sent_dict[token_id] = "{0}:{1}".format(cue_root_id, label)
                scope_root_id = token_id
                break
        #
        #
        # set other leafs to point to root
        for token_id, label in enum_labels:
            if label == "O":
                sent_dict[token_id] = "_"
            else:
                if token_id not in sent_dict.keys():
                    if inside_label:
                        label = "IN:" + label
                    if "cue" in label:
                        sent_dict[token_id] = "{0}:{1}".format(cue_root_id, label)
                    elif "scope" in label:
                        sent_dict[token_id] = "{0}:{1}".format(scope_root_id, label)
    return sent_dict

def create_conll_neg_dict(conllu_sent):
    conll_dict = {}
    for line in conllu_sent.split("\n"):
        if line != "":
            token_id = int(line.split()[0])
            conll_dict[token_id] = line
    return conll_dict

def combine_labels(token_labels):
    final_label = ""
    for l in token_labels:
        if l == "_":
            pass
        else:
            if final_label == "":
                final_label = l
            else:
                final_label += "|" + l
    if final_label == "":
        return "_"
    return final_label


def combine_neg_dicts(neg_dicts):
    combined = {}
    for i in neg_dicts[0].keys():
        labels = [s[i] for s in neg_dicts]
        final_label = combine_labels(labels)
        combined[i] = final_label
    return combined


def create_negation_conll(neg_sent,
                          setup="point_to_root",
                          inside_label=False,
                          use_dep_edges=False,
                          use_dep_labels=False
                          ):
    neg_conll = ""
    #
    sent_id = neg_sent["sent_id"]
    text = neg_sent["text"]
    negations = neg_sent["negations"]
    conll = neg_sent["conllu"]
    conll_dict = create_conll_neg_dict(conll)
    t2e = tokenidx2edge(conll)
    t2l = tokenidx2deplabel(conll)
    #
    if len(negations) > 0:
        labels = [create_labels(text, o) for o in negations]
    else:
        labels = [create_labels(text, [])]
    #
    sent_labels = [create_negation_dict(l,
                                         setup=setup,
                                         inside_label=inside_label) for l in labels]
    if use_dep_edges:
        if use_dep_labels:
            sent_labels = [redefine_root_with_dep_edges(s, t2e, t2l) for s in sent_labels]
        else:
            sent_labels = [redefine_root_with_dep_edges(s, t2e) for s in sent_labels]

    combined_labels = combine_neg_dicts(sent_labels)
    #
    for i in conll_dict.keys():
        #print(c[i] + "\t" + sd[i])
        neg_conll += conll_dict[i] + "\t" + combined_labels[i] + "\n"
    return neg_conll


def redefine_root_with_dep_edges(sent_labels, t2e, t2l=None):
    new_sent_labels = {}
    # If there are no sentiment annotations, return the current labels
    if set(sent_labels.values()) == {'_'}:
        return sent_labels
    # Find the full sentiment expression in the annotation
    exp = []
    exp_label = ""
    for idx, label in sent_labels.items():
        if "cue" in label:
            exp_label = label
            exp.append(idx)
    exp_label = exp_label.split(":")[-1]
    edges = [t2e[i] for i in exp]
    if t2l:
        deplabels = [t2l[i] for i in exp]
    else:
        deplabels = None
    #
    # given the dependency edges in the sentiment expression,
    # find the one that has an incoming edge and set as root
    root = get_const_root(exp, edges, deplabels)
    new_sent_labels[root] = "0:" + exp_label
    #
    # Do the same for the target
    targ = []
    for idx, label in sent_labels.items():
        if "scope" in label:
            targ.append(idx)
    if len(targ) > 0:
        edges = [t2e[i] for i in targ]
        if t2l:
            deplabels = [t2l[i] for i in targ]
        else:
            deplabels = None
        targ_root = get_const_root(targ, edges, deplabels)
        new_sent_labels[targ_root] = "{0}:scope".format(root)
    # Do the same for holder

    # Now iterate back through the remaining tokens in the sentiment expression
    # and set their edges pointing towards the new root, as well as the target
    # root and holder root
    for idx, label in sent_labels.items():
        if idx not in new_sent_labels:
            if "cue" in label:
                new_sent_labels[idx] = "{0}:IN:{1}".format(root, exp_label)
            elif "scope" in label:
                new_sent_labels[idx] = "{0}:IN:scope".format(targ_root)
            else:
                new_sent_labels[idx] = label
    return new_sent_labels


def tokenidx2edge(conllu):
    t2e = {}
    for line in conllu.splitlines():
        split = line.split("\t")
        idx = int(split[0])
        edge = int(split[6])
        t2e[idx] = edge
    return t2e

def tokenidx2deplabel(conllu):
    t2e = {}
    for line in conllu.splitlines():
        split = line.split("\t")
        idx = int(split[0])
        edge = split[7]
        t2e[idx] = edge
    return t2e

def get_const_root(token_ids, edges, dep_labels=None):
    # Given token ids, and dependency edges
    # return the token id which has an incoming
    # edge from outside the group
    roots = []
    labels = []
    for i, token in enumerate(token_ids):
        edge = edges[i]
        if edge not in token_ids:
            roots.append(token)
            if dep_labels:
                labels.append(dep_labels[i])
    if len(roots) > 1:
        if dep_labels:
            # If we have the dependency labels, we can use these to decide
            # which token to set as the root
            new_roots = []
            # remove any punctuation and obliques
            for root, dep_label in zip(roots, labels):
                if dep_label != "obl" and dep_label != "punct":
                    new_roots.append(root)
            if len(new_roots) > 0:
                return new_roots[0]
            else:
                return roots[0]
        else:
            # if there's no better way to tell, return the first root
            return roots[0]
    elif len(roots) == 0:
        return token_ids[0]
    else:
        return roots[0]

def sanity_check(sent_id, fine, doclevel, verbose=False):
    from pprint import pprint
    for s in fine:
        if s["sent_id"] == sent_id:
            finegrained_sent = s
    text = finegrained_sent["text"]
    opinions = finegrained_sent["opinions"]
    conll = doclevel[sent_id]
    t2e = tokenidx2edge(conll)
    t2l = tokenidx2deplabel(conll)
    #
    if len(opinions) > 0:
        labels = [create_labels(text, o) for o in opinions]
    else:
        labels = [create_labels(text, [])]
    #
    sent_labels = [create_negation_dict(l,
                                         setup="head_final",
                                         inside_label=True) for l in labels]
    if verbose:
        print("ORIGINAL:")
        print("-" * 50)
        pprint(sent_labels)
    edges_sent_labels = [redefine_root_with_dep_edges(s, t2e) for s in sent_labels]
    if verbose:
        print("EDGE Determined Roots:")
        print("-" * 50)
        pprint(edges_sent_labels)
    #return sent_labels, t2e, t2l
    labels_sent_labels = [redefine_root_with_dep_edges(s, t2e, t2l) for s in sent_labels]
    if verbose:
        print("EDGE + LABEL Determined Roots:")
        print("-" * 50)
        pprint(labels_sent_labels)
    return edges_sent_labels, labels_sent_labels


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", default="point_to_root")

    args = parser.parse_args()

    # match up fine-grained sentences with their conllu
    print("Opening Negation Data")
    with open("negation_train.json") as infile:
        train = json.load(infile)
    with open("negation_dev.json") as infile:
        dev = json.load(infile)
    with open("negation_test.json") as infile:
        test = json.load(infile)

    # filter sents with no text or annotations
    train = [s for s in train if s["text"] != ""]
    dev = [s for s in dev if s["text"] != ""]
    test = [s for s in test if s["text"] != ""]

    # tag sents
    print("Tagging datasets...")
    tag_json_files(train)
    tag_json_files(dev)
    tag_json_files(test)

    configs = [("point_to_root", False, False, False),
               ("head_first", False, False, False),
               ("head_first", True, False, False),
               ("head_final", False, False, False),
               ("head_final", True, False, False),
               ("head_final", True, True, False),
               ("head_final", True, True, True)]

    for setup, inside_label, use_dep_edges, use_dep_labels in configs:
        # covert to sentiment graphs
        train_anns = []
        for s in train:
            try:
                train_anns.append((s["sent_id"], s["text"], create_negation_conll(s, setup=setup, inside_label=inside_label, use_dep_edges=use_dep_edges, use_dep_labels=use_dep_labels)))
            except UnboundLocalError:
                print(s)
                pass

        dev_anns = []
        for s in dev:
            try:
                dev_anns.append((s["sent_id"], s["text"], create_negation_conll(s, setup=setup, inside_label=inside_label, use_dep_edges=use_dep_edges, use_dep_labels=use_dep_labels)))
            except KeyError:
                pass
            except UnboundLocalError:
                print(s)
                pass

        test_anns = []
        for s in test:
            try:
                test_anns.append((s["sent_id"], s["text"], create_negation_conll(s, setup=setup, inside_label=inside_label, use_dep_edges=use_dep_edges, use_dep_labels=use_dep_labels)))
            except KeyError:
                pass
            except UnboundLocalError:
                print(s)
                pass

        # print the datasets to file
        if inside_label:
            outdir = setup + "-inside_label"
        else:
            outdir = setup
        if use_dep_edges:
            outdir = outdir + "-dep_edges"
        if use_dep_labels:
            outdir = outdir + "-dep_labels"
        print("Saving negation graphs to {}".format(outdir))
        os.makedirs("neg_graphs/{0}".format(outdir), exist_ok=True)

        with open("neg_graphs/{0}/train.conllu".format(outdir), "w") as outfile:
            for sent_id, text, sent in train_anns:
                outfile.write("# sent_id = {0}\n".format(sent_id))
                outfile.write("# text = {0}\n".format(text))
                outfile.write(sent + "\n")

        with open("neg_graphs/{0}/dev.conllu".format(outdir), "w") as outfile:
            for sent_id, text, sent in dev_anns:
                outfile.write("# sent_id = {0}\n".format(sent_id))
                outfile.write("# text = {0}\n".format(text))
                outfile.write(sent + "\n")

        with open("neg_graphs/{0}/test.conllu".format(outdir), "w") as outfile:
            for sent_id, text, sent in test_anns:
                outfile.write("# sent_id = {0}\n".format(sent_id))
                outfile.write("# text = {0}\n".format(text))
                outfile.write(sent + "\n")
