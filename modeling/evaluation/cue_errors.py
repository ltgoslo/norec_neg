import col_data as cd
from collections import Counter
import numpy as np

def sents_are_same(gsent, psent):
    for g, p in zip(gsent, psent):
        if g.scope != p.scope:
            return False
    return True

def multiword_cues(sent):
    for l in sent:
        for scope in l.scope:
            if "cue" in scope:
                root, label = scope
                if root != 0:
                    return True
    return False

def affixal(sent):
    for l in sent:
        for scope in l.scope:
            if "cue" in scope:
                if "u" in l.form or "løs" in l.form or "fri" in l.form or "in" in l.form:
                    if l.form not in ["uten", "null"]:
                        return True
    return False


def get_only_negated(data):
    negated = {}
    for sid, sent in data.items():
        for l in sent:
            if len(l.scope) > 0:
                negated[sid] = sent
                break
    return negated

def which_gold_cues_are_missed(gold_neg, pred):
    missed_cues = Counter()
    sids = []
    for key in gold_neg.keys():
        g = gold_neg[key]
        p = pred[key]
        for i, j in zip(g, p):
            if (0, 'cue') in i.scope and (0, 'cue') not in j.scope:
                missed_cues.update([i.form])
                sids.append((key, i.form))
    return missed_cues, sids

def ave_scope_sent(sent):
    scopes = {}
    for l in sent:
        for scope in l.scope:
            if "scope" in scope:
                root, label = scope
                if root not in scopes:
                    scopes[root] = 1
                else:
                    scopes[root] += 1
    return scopes

def ave_scope_length(pred_neg):
    lengths = []
    for sid, sent in pred_neg.items():
        scopes = ave_scope_sent(sent)
        for scope in scopes.values():
            lengths.append(scope)
    return np.mean(lengths)



def discontinuous(sent):
    scopes = {}
    for l in sent:
        for scope in l.scope:
            if "scope" in scope:
                root, label = scope
                if root not in scopes:
                    scopes[root] = [root, l.id]
                else:
                    scopes[root].append(l.id)
    for scope in scopes.values():
        scope = sorted(scope)
        #print(scope)
        for i, j in enumerate(scope):
            if i < len(scope) - 1:
                next_n = scope[i+1]
                dist = next_n - j
                #print(dist)
                if dist > 1:
                    return True
    return False


if __name__ == "__main__":

    gold = dict([(l.id, l) for l in cd.read_col_data("../data/neg_graphs/point_to_root/test.conllu")])
    pred = dict([(l.id, l) for l in cd.read_col_data("../experiments/point_to_root/2/test.conllu.pred")])

    gold_neg = get_only_negated(gold)
    pred_neg = get_only_negated(pred)

    # which cues in gold but not predicted?
    print("Which cues in gold but not predicted?")
    gmissed, gsids = which_gold_cues_are_missed(gold_neg, pred)
    for cue, count in gmissed.most_common():
        print("-- {}:{}".format(cue, count))

    # --subquestion: does the model EVER predict these cues?
    never_predicted = [cue for cue in gmissed]
    for sent_id, sent in pred_neg.items():
        for l in sent:
            if (0, "cue") in l.scope:
                if l.form in never_predicted:
                    never_predicted.remove(l.form)
    print("Model never predicts:")
    for cue in never_predicted:
        print("-- {}".format(cue))

    print()
    print("-" * 80)
    print()

    # which cues in pred but not in gold?
    print("Which cues in pred but not in gold?")
    pmissed, psids = which_gold_cues_are_missed(pred_neg, gold)
    for cue, count in pmissed.most_common():
        print("-- {}:{}".format(cue, count))


    print()
    print("-" * 80)
    print()

    # average length of gold vs predicted scopes?
    print("Ave len gold scopes: {0:.1f}".format(ave_scope_length(gold_neg)))
    print("Ave len pred scopes: {0:.1f}".format(ave_scope_length(pred_neg)))

    print()
    print("-" * 80)
    print()

    #How well does it handle discontinuous scope?
    gdisc = [(sid, sent) for sid, sent in gold_neg.items() if discontinuous(sent)]
    pdisc = [pred[sid] for sid, sent in gdisc]
    incorrect = [(sid, gsent, psent) for (sid, gsent), psent in zip(gdisc, pdisc) if not sents_are_same(gsent, psent)]

    print("Precent discontinuous scope error: {0:.1f}".format(len(incorrect) / len(gdisc) * 100))

    # How does the model deal with affixal cues?
    gaffixal = [(sid, sent) for sid, sent in gold_neg.items() if affixal(sent)]
    paffixal = [(sid, pred[sid]) for sid, sent in gaffixal]
    affixal_incorrect = [(sid, gsent, psent) for (sid, gsent), (sid2, psent) in zip(gaffixal, paffixal) if not sents_are_same(gsent, psent)]

    print("Precent affixal scope error: {0:.1f}".format(len(affixal_incorrect) / len(gaffixal) * 100))

    gaffixal = dict([(sid, sent) for sid, sent in gaffixal])
    paffixal = dict([(sid, sent) for sid, sent in paffixal])
    print("Ave len gold affixal scopes: {0:.1f}".format(ave_scope_length(gold_neg)))
    print("Ave len pred affixal scopes: {0:.1f}".format(ave_scope_length(pred_neg)))
